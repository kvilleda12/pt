# pt/backend/llm/patient_context.py
from __future__ import annotations

from datetime import date, datetime
from typing import Tuple, Optional, Dict, Any

from sqlalchemy.orm import Session
from backend.database.database import SessionLocal, User, ProblemReport

def _safe_close(db: Session):
    try:
        db.close()
    except Exception:
        pass

def _compute_age_years(dob: Optional[date | datetime]) -> Optional[int]:
    if not dob:
        return None
    if isinstance(dob, datetime):
        dob = dob.date()
    today = date.today()
    years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return max(0, years)

def _extract_report_label_code(report: ProblemReport) -> Optional[str]:
    """
    body_part_id is an Enum in your schema. Handle common cases:
    - Enum: .value or .name
    - direct str
    """
    if report is None:
        return None
    value = getattr(report.body_part_id, "value", None)
    if isinstance(value, str) and value:
        return value.lower()
    name = getattr(report.body_part_id, "name", None)
    if isinstance(name, str) and name:
        return name.lower()
    if isinstance(report.body_part_id, str):
        return report.body_part_id.lower()
    return None

def _compose_context_string(user: User, report: Optional[ProblemReport], age_years: Optional[int]) -> str:
    parts = []
    if user and user.name:
        parts.append(f"- Patient Name: {user.name}")
    if age_years is not None:
        parts.append(f"- Patient Age: {age_years}")

    if report:
        label_text = _extract_report_label_code(report) or "e"
        parts.append(f"- Primary Complaint: Pain or concern in body-part code '{label_text}'.")
        parts.append(f"- Had this problem before: {bool(report.had_this_problem_before)}")
        parts.append(f"- Prior PT history: {bool(report.had_physical_therapy_before)}")
        if report.what_helped_before:
            parts.append(f"- Previously helpful: {report.what_helped_before}")
        if report.previous_unrelated_problem:
            parts.append(f"- Other relevant history: {report.previous_unrelated_problem}")
        # Patient Lived Experience
        if report.opinion_cause:
            parts.append(f"- Patient believes the cause: {report.opinion_cause}")
        if report.pain_worse:
            parts.append(f"- Pain worse with: {report.pain_worse}")
        if report.pain_better:
            parts.append(f"- Pain better with: {report.pain_better}")
        if report.goal_for_pt:
            parts.append(f"- Patient goal: {report.goal_for_pt}")
    else:
        parts.append("No problem report on file.")

    return "\n".join(parts)

def build_user_context(
    *,
    user_id: Optional[int] = None,
    email: Optional[str] = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Returns (context_string, context_meta)
    context_meta contains:
      - user_id, email, age_years, age_group
      - report_label_code (e.g., 'ra', 'n', etc.)
      - had_pt_before, had_this_problem_before
      - goal_for_pt, what_helped_before
    """
    db: Session = SessionLocal()
    try:
        user: Optional[User] = None
        if user_id is not None:
            user = db.query(User).filter(User.id == user_id).first()
        elif email is not None:
            user = db.query(User).filter(User.email == email).first()

        if not user:
            return ("No user found.", {"user_id": user_id, "email": email})

        # Latest report
        report: Optional[ProblemReport] = (
            db.query(ProblemReport)
            .filter(ProblemReport.user_id == user.id)
            .order_by(ProblemReport.id.desc())
            .first()
        )

        age_years = _compute_age_years(user.date_of_birth)
        age_group = "older_adult" if (age_years is not None and age_years >= 65) else "adult"

        report_label_code = _extract_report_label_code(report) if report else None

        ctx_string = _compose_context_string(user, report, age_years)
        ctx_meta: Dict[str, Any] = {
            "user_id": user.id,
            "email": user.email,
            "age_years": age_years,
            "age_group": age_group,
            "report_label_code": report_label_code,
            "had_pt_before": bool(getattr(report, "had_physical_therapy_before", False)) if report else False,
            "had_this_problem_before": bool(getattr(report, "had_this_problem_before", False)) if report else False,
            "goal_for_pt": getattr(report, "goal_for_pt", None) if report else None,
            "what_helped_before": getattr(report, "what_helped_before", None) if report else None,
        }
        return ctx_string, ctx_meta
    finally:
        _safe_close(db)
