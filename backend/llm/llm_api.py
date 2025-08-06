
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from backend.llm.chatbot import get_user_data_from_db

#key stored in env
load_dotenv()

# router to the main api
router = APIRouter()

# Define the data structure for incoming chat messages
class ChatMessageInput(BaseModel):
    message: str
    # user_id: int. Once needed and we can test

# Initialize the Groq LLM
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.7)

class ChatMessageInput(BaseModel):
    message: str
    user_profile_context: str # The context is now sent from the frontend

class UserContextRequest(BaseModel):
    user_id: int


#once the session begins we get the users info
@router.post("/get_context")
async def get_user_context(request: UserContextRequest):
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
# endpoint allowing us to interact
@router.post("/chat")
async def handle_chat_message(input: ChatMessageInput):

    template = """
    You are an expert AI physical therapy assistant. Always consider the user's profile context provided below before answering.

    ---
    USER PROFILE CONTEXT:
    {user_profile_context}
    ---

    USER'S QUESTION:
    {question}

    YOUR RESPONSE:
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "user_profile_context": input.user_profile_context,
        "question": input.message
    })
    
    return {"response": response}

