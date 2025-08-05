import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Load .env variables

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_caption(caption):
    timestamp = datetime.utcnow().isoformat()
    data = {
        "caption": caption,
        "timestamp": timestamp,
        # optionally add user_id, session_id, etc.
    }
    response = supabase.table("captions").insert(data).execute()
    if response.error:
        print(f"Error storing caption: {response.error}")
    else:
        print("Caption stored successfully.")

def store_summary(summary_text):
    timestamp = datetime.utcnow().isoformat()
    data = {
        "summary": summary_text,
        "timestamp": timestamp,
        # optionally add user_id, session_id, etc.
    }
    response = supabase.table("summaries").insert(data).execute()
    if response.error:
        print(f"Error storing summary: {response.error}")
    else:
        print("Summary stored successfully.")
