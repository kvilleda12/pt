# pt/backend/llm/prompts.py
from langchain.prompts import PromptTemplate

# Multi-query expansion prompt
MULTI_QUERY_PROMPT = PromptTemplate.from_template(
    """You rewrite a user query into diverse search queries for a physical-therapy exercise library.
User query: {query}

Rewrite it into {n_variants} diverse search queries covering:
- synonyms and layperson terms,
- likely specific body-part labels (left/right if implied),
- type variations (stretch, mobility, isometric, strengthening),
- equipment/no-equipment variants.

Return each on a new line, with no numbering, no quotes, no extra text."""
)

# HyDE prompt: generate a short hypothetical answer (used as another retrieval query)
HYDE_PROMPT = PromptTemplate.from_template(
    """Write a short, neutral, technical description of the exercises that would answer:
"{query}"
Aim for 3-5 sentences with body part names, action verbs, and common PT phrasing; no fluff."""
)

# Final synthesis prompt: builds the answer from retrieved docs (+ user profile)
FINAL_ANSWER_PROMPT = PromptTemplate.from_template(
    """You are an expert physical therapy assistant. Consider the patient's context and the retrieved exercise cards.
Only propose safe, clearly-instructed exercises. Choose the best {n_recs} options.

PATIENT PROFILE CONTEXT (may be empty):
{user_context}

AGE-AWARE GUIDANCE:
{age_instructions}

RETRIEVED EXERCISE CARDS (ID | NAME | BODY_PART | TYPE | EQUIPMENT):
{cards_brief}

INSTRUCTIONS:
- Start with a 1–2 sentence empathetic summary tailored to the profile (if provided).
- Then list {n_recs} exercises. For each: show **Name** (ID), **What it helps**, **Equipment**, and **Step-by-step** (3–6 bullets from the card). Keep steps concrete and actionable.
- Prefer matching body part(s) and constraints implied by the user query.
- If left/right is specified by the user, tailor cues accordingly.
- Adjust difficulty by age if needed (use seated, low-impact, slower progressions for older adults).
- End with a brief safety note.

USER QUESTION:
{question}

Answer:"""
)

