import json
import re
from pathlib import Path
import requests
from typing import Any, Dict
from config import OLLAMA_API_URL, OLLAMA_MODEL, OLLAMA_TEMPERATURE, OLLAMA_MAX_TOKENS, AUDITS_DIR, DEFAULT_CRITERIA
from storage import update_link_fields
from labels import LABEL_CODES
from logger import log

SYSTEM_PROMPT = "You are a strict information quality reviewer for a physical therapy instruction corpus. Return JSON only."
USER_PROMPT_TEMPLATE = """Task: Evaluate if the page content is VIABLE for precise physical-therapy instructions.

Criteria:
- The text must describe specific PT exercises or stretches, with clear steps, cues, reps/sets, or safety notes.
- Avoid vague wellness content without actionable steps.
- Prefer medically sound terminology and accurate anatomy.
- Reject sales pages, thin content, or unrelated topics.

Custom criteria (JSON):
{criteria_json}

Body-part labels (codes → names):
n: neck, c: chest, ls: left shoulder, rs: right shoulder, lt: left tricep, rt: right tricep,
lb: left bicep, rb: right bicep, a: abdomen, b: back, lh: left hamstring, rh: right hamstring,
lq: left quadriceps, rq: right quadriceps, lc: left calf, rc: right calf, la: left ankle, ra: right ankle, e: full body.

Output JSON schema (strict):
{
  "viable": true|false,
  "confidence": float,
  "reason": "short reason",
  "labels": ["n","c","ls","rs","lt","rt","lb","rb","a","b","lh","rh","lq","rq","lc","rc","la","ra","e"]
}

Page text (begin):
\"\"\"{page_text}\"\"\"
Page text (end).
Return ONLY the JSON. No extra text.
"""

def _ollama_call(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"<<SYS>>{SYSTEM_PROMPT}<<SYS>>\n{prompt}",
        "stream": False,
        "options": {"temperature": OLLAMA_TEMPERATURE, "num_predict": OLLAMA_MAX_TOKENS}
    }
    log(f"[LLM] Calling Ollama model={OLLAMA_MODEL}")
    r = requests.post(OLLAMA_API_URL, json=payload, timeout=120, headers={"Accept": "application/json"})
    r.raise_for_status()
    body = r.text or ""
    log(f"[LLM] Ollama returned {len(body)} bytes")
    return body

def _response_to_text(body: str) -> str:
    body = body.strip()
    if not body:
        return ""
    if body.startswith("{"):
        try:
            obj = json.loads(body)
            if isinstance(obj, dict) and "response" in obj:
                return obj.get("response", "")
        except Exception:
            pass
    lines = [ln for ln in body.splitlines() if ln.strip()]
    if all(ln.strip().startswith("{") for ln in lines):
        acc = []
        for ln in lines:
            try:
                obj = json.loads(ln)
                if isinstance(obj, dict) and "response" in obj:
                    acc.append(obj["response"])
            except Exception:
                continue
        if acc:
            return "\n".join(acc)
    return body

def _extract_json_block(s: str) -> Dict[str, Any]:
    s = s.strip()
    s = re.sub(r"^```(?:json)?|```$", "", s, flags=re.I|re.M).strip()
    depth = 0
    start = None
    for i, ch in enumerate(s):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    block = s[start:i+1]
                    try:
                        return json.loads(block)
                    except Exception:
                        continue
    m = re.search(r"\{[\s\S]*\}", s)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return {}
    return {}

def _heuristic(text: str, criteria: Dict[str, Any]) -> Dict[str, Any]:
    if not text or len(text) < int(criteria.get("min_text_len", 500)):
        return {"viable": False, "confidence": 0.3, "reason": "too short", "labels": []}
    kws = [k.lower() for k in criteria.get("keywords_any", [])]
    has_kw = any(k in text.lower() for k in kws) if kws else True
    rej = [r.lower() for r in criteria.get("reject_phrases_any", [])]
    has_reject = any(r in text.lower() for r in rej)
    viable = bool(has_kw and not has_reject)
    return {"viable": viable, "confidence": 0.55 if viable else 0.35, "reason": "heuristic pass" if viable else "heuristic reject", "labels": []}

def classify_text(doc_id: str, text: str, criteria: Dict[str, Any] = None) -> Dict[str, Any]:
    criteria = criteria or DEFAULT_CRITERIA
    snippet = text[:20000]
    raw_text = ""
    try:
        user = USER_PROMPT_TEMPLATE.format(criteria_json=json.dumps(criteria, ensure_ascii=False), page_text=snippet)
        log(f"[CLASSIFY] id={doc_id[:8]} sending {len(snippet)} chars to Mistral")
        body = _ollama_call(user)
        raw_text = _response_to_text(body)
        parsed = _extract_json_block(raw_text)
        used_heuristic = False
        if parsed.get("viable") is None:
            used_heuristic = True
            parsed = _heuristic(snippet, criteria)
        viable = bool(parsed.get("viable", False))
        confidence = float(parsed.get("confidence", 0.0))
        reason = str(parsed.get("reason", ""))[:500]
        labels = [l for l in parsed.get("labels", []) if isinstance(l, str) and l in LABEL_CODES]
        update_link_fields(doc_id, viable=viable, confidence=confidence, reason=reason, labels=labels)
        Path(AUDITS_DIR, f"{doc_id}_ollama_raw.txt").write_text(raw_text, encoding="utf-8")
        Path(AUDITS_DIR, f"{doc_id}.json").write_text(
            json.dumps({"doc_id": doc_id, "classification": {"viable": viable, "confidence": confidence, "reason": reason, "labels": labels}}, indent=2),
            encoding="utf-8"
        )
        log(f"[CLASSIFY] id={doc_id[:8]} viable={viable} conf={confidence:.2f} labels={labels} {'(heuristic)' if used_heuristic else '(llm)'}")
        return {"viable": viable, "confidence": confidence, "reason": reason, "labels": labels}
    except Exception as e:
        parsed = _heuristic(snippet, criteria)
        update_link_fields(doc_id, viable=parsed["viable"], confidence=parsed["confidence"], reason="LLM error; heuristic used", labels=parsed["labels"])
        Path(AUDITS_DIR, f"{doc_id}_ollama_raw.txt").write_text(raw_text, encoding="utf-8")
        Path(AUDITS_DIR, f"{doc_id}.json").write_text(
            json.dumps({"doc_id": doc_id, "classification": parsed}, indent=2),
            encoding="utf-8"
        )
        log(f"[CLASSIFY] id={doc_id[:8]} LLM ERROR -> heuristic ({e})")
        return parsed
