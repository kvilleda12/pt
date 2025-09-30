
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from .settings import BASE_DIR, EXERCISES_CANDIDATES

def load_exercises_json() -> Dict:
    """
    Load the exercises JSON
    Returns the raw dict with keys: metadata, exercises
    """
    for name in EXERCISES_CANDIDATES:
        path = BASE_DIR / name
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)
    raise FileNotFoundError(f"Could not find any of: {EXERCISES_CANDIDATES} in {BASE_DIR}")

def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())

def build_label_maps(meta: Dict) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Returns (code->name, name->code) maps using metadata.label_map if present.
    """
    label_map = meta.get("label_map", {})
    code_to_name = {k: v for k, v in label_map.items()}
    name_to_code = {v: k for k, v in code_to_name.items()}
    # Fallback if missing
    if not code_to_name:
        code_to_name = {
            'n':'neck','c':'chest','ls':'left_shoulder','rs':'right_shoulder',
            'lt':'left_tricep','rt':'right_tricep','lb':'left_bicep','rb':'right_bicep',
            'a':'abdomen','b':'back','lh':'left_hamstring','rh':'right_hamstring',
            'lq':'left_quadriceps','rq':'right_quadriceps','lc':'left_calf','rc':'right_calf',
            'la':'left_ankle','ra':'right_ankle','e':'everything_general'
        }
        name_to_code = {v:k for k,v in code_to_name.items()}
    return code_to_name, name_to_code

def guess_labels_from_query(q: str, name_to_code: Dict[str, str]) -> List[str]:
    """
    Heuristic label guesser to help filtering/boosting during retrieval.
    We match synonyms for sides and parts, mapping to your codes.
    """
    qn = normalize(q)

    side_map = {
        "left": "left", "right": "right", "l ": "left", "r ": "right", "l-": "left", "r-": "right",
        "l/": "left", "r/": "right"
    }

    part_synonyms = {
        "neck": ["neck", "cervical"],
        "chest": ["chest", "pec", "pectoralis", "thorax"],
        "shoulder": ["shoulder", "rotator cuff", "deltoid", "scapular", "scapula"],
        "tricep": ["tricep", "triceps"],
        "bicep": ["bicep", "biceps"],
        "abdomen": ["abdomen", "abdominal", "core", "stomach"],
        "back": ["back", "lumbar", "thoracic", "spine"],
        "hamstring": ["hamstring", "posterior thigh"],
        "quadriceps": ["quad", "quadriceps", "anterior thigh"],
        "calf": ["calf", "gastrocnemius", "soleus"],
        "ankle": ["ankle", "achilles", "foot and ankle", "dorsiflexion", "plantarflexion"],
        "everything_general": ["full body", "whole body", "entire body", "all over", "general"]
    }

    # Decide side (left/right) if user mentions
    side = None
    for key, val in side_map.items():
        if f"{key} " in qn or qn.startswith(key):
            side = val
            break

    targets = []
    # find part
    for part, syns in part_synonyms.items():
        if any(s in qn for s in syns):
            # map to your codes via name_to_code
            if part == "shoulder":
                if side == "left":
                    targets.append(name_to_code.get("left_shoulder"))
                elif side == "right":
                    targets.append(name_to_code.get("right_shoulder"))
                else:
                    # both shoulders useful for retrieval expansion
                    targets += [name_to_code.get("left_shoulder"), name_to_code.get("right_shoulder")]
            elif part == "tricep":
                targets.append(name_to_code.get(f"{side or 'left'}_tricep")) if side else \
                    targets.extend([name_to_code.get("left_tricep"), name_to_code.get("right_tricep")])
            elif part == "bicep":
                targets.append(name_to_code.get(f"{side or 'left'}_bicep")) if side else \
                    targets.extend([name_to_code.get("left_bicep"), name_to_code.get("right_bicep")])
            elif part == "hamstring":
                targets.append(name_to_code.get(f"{side or 'left'}_hamstring")) if side else \
                    targets.extend([name_to_code.get("left_hamstring"), name_to_code.get("right_hamstring")])
            elif part == "quadriceps":
                targets.append(name_to_code.get(f"{side or 'left'}_quadriceps")) if side else \
                    targets.extend([name_to_code.get("left_quadriceps"), name_to_code.get("right_quadriceps")])
            elif part == "calf":
                targets.append(name_to_code.get(f"{side or 'left'}_calf")) if side else \
                    targets.extend([name_to_code.get("left_calf"), name_to_code.get("right_calf")])
            elif part == "ankle":
                targets.append(name_to_code.get(f"{side or 'left'}_ankle")) if side else \
                    targets.extend([name_to_code.get("left_ankle"), name_to_code.get("right_ankle")])
            else:
                targets.append(name_to_code.get(part))
    # Dedup + drop Nones
    return [t for t in dict.fromkeys(targets) if t]
