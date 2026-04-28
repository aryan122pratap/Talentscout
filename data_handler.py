"""Handles local JSON storage and GDPR compliance for candidate data."""
import json
import os
import uuid
from datetime import datetime
from config import DATA_FILE

DATA_PRIVACY_NOTICE = (
    "🔒 **Data Privacy Notice:** By continuing, you agree to allow TalentScout "
    "to collect your name, contact info, and technical responses. This data is strictly "
    "used for recruitment purposes and stored securely. We do not sell your data."
)

def init_db() -> None:
    """Initializes the local JSON database file if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def save_candidate(candidate_info: dict, tech_stack: list, qa_pairs: list) -> None:
    """
    Saves complete candidate data to the local JSON file.
    
    Args:
        candidate_info (dict): Basic info collected.
        tech_stack (list): Extracted technologies.
        qa_pairs (list): Questions and answers.
    """
    init_db()
    
    record = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "name": candidate_info.get("name", ""),
        "email": candidate_info.get("email", ""),
        "phone": candidate_info.get("phone", ""),
        "experience_years": candidate_info.get("experience", ""),
        "desired_position": candidate_info.get("position", ""),
        "location": candidate_info.get("location", ""),
        "tech_stack": tech_stack,
        "qa_pairs": qa_pairs,
        "data_consent": True
    }
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []
        
    data.append(record)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def anonymize_candidate(candidate_dict: dict) -> dict:
    """
    Masks PII (email, phone) for secure logging or display.
    
    Args:
        candidate_dict (dict): Raw candidate data.
        
    Returns:
        dict: Anonymized candidate data.
    """
    anonymized = candidate_dict.copy()
    if "email" in anonymized and "@" in anonymized["email"]:
        name, domain = anonymized["email"].split("@")
        anonymized["email"] = f"{name[0]}***@{domain}"
    if "phone" in anonymized and len(anonymized["phone"]) >= 4:
        anonymized["phone"] = f"***-***-{anonymized['phone'][-4:]}"
    return anonymized