"""Utility functions for validation, formatting, and analysis."""
import re
from typing import List
from config import FRUSTRATION_KEYWORDS

def validate_email(email: str) -> bool:
    """
    Validates an email address using a standard regular expression.
    
    Args:
        email (str): The email string to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))

def validate_phone(phone: str) -> bool:
    """
    Validates a phone number (allows +, spaces, dashes, minimum 10 digits).
    
    Args:
        phone (str): The phone string to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    # Remove allowed non-digit characters
    digits_only = re.sub(r'[\+\-\s\(\)]', '', phone)
    return len(digits_only) >= 10 and digits_only.isdigit()

def validate_experience(experience: str) -> bool:
    """
    Validates that the experience is a valid positive number.
    
    Args:
        experience (str): The experience string to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        val = float(experience)
        return val >= 0
    except ValueError:
        return False

def detect_frustration(text: str) -> bool:
    """
    Detects signs of frustration in user text using a keyword-based approach.
    
    Args:
        text (str): The user's input text.
        
    Returns:
        bool: True if frustration keywords are found, False otherwise.
    """
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in FRUSTRATION_KEYWORDS)

def format_interview_summary(candidate_info: dict, qa_pairs: List[dict]) -> str:
    """
    Formats the collected data and Q&A pairs into a readable text summary.
    
    Args:
        candidate_info (dict): Collected candidate details.
        qa_pairs (List[dict]): List of Q&A dictionaries.
        
    Returns:
        str: Formatted interview summary.
    """
    summary = "🎯 TALENTSCOUT INTERVIEW SUMMARY 🎯\n"
    summary += "="*35 + "\n\n"
    summary += "CANDIDATE INFORMATION:\n"
    summary += "-"*25 + "\n"
    for key, value in candidate_info.items():
        if value:
            clean_key = key.replace("_", " ").title()
            summary += f"{clean_key}: {value}\n"
    
    summary += "\nTECHNICAL ASSESSMENT:\n"
    summary += "-"*25 + "\n"
    for idx, pair in enumerate(qa_pairs, 1):
        summary += f"\n[Technology: {pair['technology']}]\n"
        summary += f"Q: {pair['question']}\n"
        summary += f"A: {pair['answer']}\n"
    
    summary += "\n" + "="*35 + "\n"
    summary += "End of Report"
    return summary