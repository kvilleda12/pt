from datetime import datetime

_current_session = None

class SessionManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.captions = []
        self.start_time = datetime.now()

    def log_caption(self, caption):
        timestamp = datetime.now().isoformat()
        self.captions.append({"timestamp": timestamp, "caption": caption})
        print(f"[{timestamp}] Caption logged: {caption}")

    def summarize_session(self):
        summary = " ".join([c["caption"] for c in self.captions])
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds() / 60
        return (f"User: {self.user_id}\nDuration: {duration:.2f} minutes\nSummary: {summary}")

def start_session(user_id):
    global _current_session
    _current_session = SessionManager(user_id)
    print(f"Session started for user {user_id}")

def log_caption(caption):
    if _current_session is None:
        raise Exception("No active session. Call start_session first.")
    _current_session.log_caption(caption)

def end_session():
    if _current_session is None:
        raise Exception("No active session. Call start_session first.")
    return _current_session.summarize_session()
