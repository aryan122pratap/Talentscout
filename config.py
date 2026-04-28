"""Configuration constants for the TalentScout chatbot."""
import os

# Application Info
APP_NAME = "TalentScout"
APP_SUBTITLE = "AI Hiring Assistant"
DATA_FILE = "candidates_data.json"

# LLM Configuration (Updated for Groq)
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_TOKENS = 1024
TEMPERATURE = 0.7

# Conversation Stages
STAGES = [
    "GREETING",
    "COLLECT_NAME",
    "COLLECT_EMAIL",
    "COLLECT_PHONE",
    "COLLECT_EXPERIENCE",
    "COLLECT_POSITION",
    "COLLECT_LOCATION",
    "COLLECT_TECH_STACK",
    "TECHNICAL_QUESTIONS",
    "FAREWELL"
]

# Progress Mapping for Sidebar
PROGRESS_MAP = {
    "GREETING": 0,
    "COLLECT_NAME": 10,
    "COLLECT_EMAIL": 20,
    "COLLECT_PHONE": 30,
    "COLLECT_EXPERIENCE": 40,
    "COLLECT_POSITION": 50,
    "COLLECT_LOCATION": 60,
    "COLLECT_TECH_STACK": 70,
    "TECHNICAL_QUESTIONS": 85,
    "FAREWELL": 100
}

# Exit Keywords
EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye", "end", "stop"}

# Sentiment Keywords (Frustration)
FRUSTRATION_KEYWORDS = {
    "don't know", "not sure", "confused", "terrible", "hard", 
    "difficult", "stuck", "frustrating", "give up", "lost"
}