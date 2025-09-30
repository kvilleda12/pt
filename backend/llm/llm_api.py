# pt/backend/llm/llm_api.py
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

from backend.llm.chatbot import get_user_data_from_db
from backend.llm.rag_chain import answer_with_rag
from backend.llm.patient_context import build_user_context

load_dotenv()
router = APIRouter()

class ChatMessageInput(BaseModel):
    message: str
    # Either the FE passes the context...
    user_profile_context: str | None = None
    # ...or we can build it here from user_id or email:
    user_id: int | None = None
    email: str | None = None

class UserContextRequest(BaseModel):
    user_id: int

@router.post("/get_context")
async def get_user_context(request: UserContextRequest):
    # (You can keep this legacy route if FE wants an explicit call)
    user_data = get_user_data_from_db(request.user_id)
    if not user_data or not user_data.get("report"):
        return {"context": "No problem report has been filed for this user yet."}

    report = user_data["report"]
    context_parts = [
        f"- Primary Complaint: Pain in the {report.body_part_id.name}.",
        f"- Patient has experienced this problem before: {report.had_this_problem_before}.",
        f"- Past successful treatments include: {report.what_helped_before or 'N/A'}.",
        f"- Patient has a history of receiving physical therapy: {report.had_physical_therapy_before}.",
        f"- Other relevant history: {report.previous_unrelated_problem or 'N/A'}."
    ]
    context_window = "\n".join(context_parts)
    return {"context": context_window}

@router.post("/chat")
async def handle_chat_message(input: ChatMessageInput):
    """
    RAG endpoint that:
    - Builds (or accepts) patient context,
    - Reads age & primary body-part from DB to bias retrieval and instructions,
    - Runs RAG Fusion retrieval + structured synthesis.
    """
    # 1) Build context if not supplied
    user_context = input.user_profile_context
    force_labels: list[str] | None = None
    age_years: int | None = None

    if not user_context:
        ctx_string, ctx_meta = build_user_context(
            user_id=input.user_id,
            email=input.email
        )
        user_context = ctx_string
        # Pull structured bits for retrieval/prompt
        report_label = ctx_meta.get("report_label_code")
        if report_label:
            force_labels = [report_label]
        age_years = ctx_meta.get("age_years")

    # 2) Answer with RAG
    response = answer_with_rag(
        user_context=user_context or "",
        user_question=input.message,
        force_labels=force_labels,
        age_years=age_years
    )
    return {"response": response}
