# pt/backend/llm/rag_chain.py (only the parts that change)
from typing import List, Optional
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .settings import (
    MAX_TOKENS, TEMPERATURE, TOP_K_FINAL, SAFETY_DISCLAIMER
)
from .ingest import build_or_load_vectorstore
from .utils import load_exercises_json, build_label_maps, guess_labels_from_query
from .retrieval import retrieve_fused
from .prompts import FINAL_ANSWER_PROMPT

_vectorstore = build_or_load_vectorstore()
_all_docs = _vectorstore.similarity_search("health", k=1_000_000)

def _cards_brief(docs: List[Document]) -> str:
    lines = []
    for d in docs:
        md = d.metadata
        lines.append(f"{md.get('id')} | {md.get('name')} | {md.get('body_part')} | {md.get('type')} | {md.get('equipment')}")
    return "\n".join(lines[:TOP_K_FINAL])

def _age_instructions(age_years: Optional[int]) -> str:
    if age_years is None:
        return "None."
    if age_years >= 65:
        return (
            "Patient may benefit from gentler progressions, slower tempo, longer rest, and options for seated or supported balance. "
            "Avoid sudden direction changes and heavy loads; emphasize safety, posture, and pain-free ranges."
        )
    return "Use standard adult progressions."

def answer_with_rag(
    user_context: str,
    user_question: str,
    *,
    force_labels: Optional[List[str]] = None,
    age_years: Optional[int] = None
) -> str:
    data = load_exercises_json()
    code_to_name, name_to_code = build_label_maps(data.get("metadata", {}))

    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=TEMPERATURE, max_tokens=MAX_TOKENS)

    # Guess + merge labels
    guessed_labels = guess_labels_from_query(user_question, name_to_code)
    label_filter = list({*(guessed_labels or []), *(force_labels or [])})

    fused_docs = retrieve_fused(
        llm=llm,
        vectorstore=_vectorstore,
        all_docs=_all_docs,
        query=user_question,
        label_filter=label_filter or None,
    )
    top_docs = fused_docs[:TOP_K_FINAL]

    # Build final prompt text
    final_prompt = FINAL_ANSWER_PROMPT.format(
        n_recs=min(3, len(top_docs)),
        user_context=user_context or "(no profile data provided)",
        age_instructions=_age_instructions(age_years),
        cards_brief=_cards_brief(top_docs),
        question=user_question,
    )

    # Call the model directly with the string
    raw_response = llm.invoke(final_prompt)
    answer = StrOutputParser().invoke(raw_response)

    return f"{answer}\n\n**Safety:** {SAFETY_DISCLAIMER}"