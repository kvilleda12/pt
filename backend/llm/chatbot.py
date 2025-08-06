import os
from dotenv import load_dotenv


from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from sqlalchemy.orm import Session
from backend.database.database import User, ProblemReport
from backend.database.database import SessionLocal

load_dotenv() 

#get the user from the database
def get_user_data_from_db(user_id: int) -> dict | None:
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
            

        latest_report = db.query(ProblemReport).filter(ProblemReport.user_id == user_id).order_by(ProblemReport.id.desc()).first()

        return {"user": user, "report": latest_report}
    finally:
        db.close()

# --- 2. The Core LLM Logic (Upgraded) ---
def generate_contextual_response(user_id: int) -> str:

    print(f"--- Generating contextual response for user_id: {user_id} ---")
    
    data = get_user_data_from_db(user_id)
    
    if not data or not data.get("user"):
        return "Could not find user information."

    user = data["user"]
    report = data["report"]
    
    # build the context for the bot. This basically just gives more inrtmation to the model when querying
    context_parts = []
    if report:
        if report.body_part_id:
            context_parts.append(f"- Primary Complaint: Pain in the {report.body_part_id.name}.") # Use .name for Enums
        if report.had_this_problem_before:
            context_parts.append("- Patient has experienced this problem before.")
            if report.what_helped_before:
                context_parts.append(f"- Past successful treatments include: {report.what_helped_before}.")
        if report.had_physical_therapy_before:
            context_parts.append("- Patient has a history of receiving physical therapy.")
        if report.previous_unrelated_problem:
            context_parts.append(f"- Other relevant history: {report.previous_unrelated_problem}.")
    else:
        context_parts.append("No problem report has been filed for this user yet.")

    context_window = "\n".join(context_parts)
    
    #initizalize
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.7)
    
    # NEEDS FIXING. WE NEED TO PLAY AROUND WITH POMPTS FOR BETTER USAGE
    template = """
    You are an expert AI physical therapy assistant. You are speaking to a patient named {name}.
    Your task is to provide an empathetic and professional opening statement based on their submitted problem report.

    Summarize their situation to show you understand, and end by telling them you are ready to help them find some safe and effective exercises. Do not suggest any exercises yet.

    PATIENT NAME: {name}
    
    PROBLEM REPORT CONTEXT:
    {context_window}
    """
    prompt_template = ChatPromptTemplate.from_template(template)
    
    chain = prompt_template | llm | StrOutputParser()
    
    response = chain.invoke({
        "name": user.name,
        "context_window": context_window
    })
    
    return response

# test
if __name__ == "__main__":
    print("Running chatbot.py directly for testing...")
    
    # Simulate a logged-in user with ID 1
    contextual_response = generate_contextual_response(user_id=1)
    
    print("\n--- FINAL OUTPUT ---")
    print(contextual_response)