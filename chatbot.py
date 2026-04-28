"""Core chatbot logic, state machine, and Groq LLM integration."""
import os
from groq import Groq
from typing import Tuple

from config import PROGRESS_MAP, EXIT_KEYWORDS, MODEL_NAME, TEMPERATURE, MAX_TOKENS
from prompts import (
    SYSTEM_PROMPT, TECH_QUESTION_PROMPT, FALLBACK_PROMPT,
    TECH_EXTRACTION_PROMPT
)
from utils import (
    validate_email, validate_phone, validate_experience, detect_frustration
)
from data_handler import save_candidate, DATA_PRIVACY_NOTICE

class TalentScoutChatbot:
    """Main Chatbot Class handling state and AI interactions."""
    
    def __init__(self):
        """Initializes the chatbot state and Groq API client."""
        self.stage = "COLLECT_NAME"
        self.candidate_info = {
            "name": "", "email": "", "phone": "", 
            "experience": "", "position": "", "location": ""
        }
        self.tech_stack = []
        self.current_tech_index = 0
        self.current_questions = ""
        self.qa_pairs = []
        
        # Configure the Groq SDK
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment.")
        self.client = Groq(api_key=api_key)

    def get_initial_greeting(self) -> str:
        """Returns the very first message the bot sends."""
        return (f"Hello! I am the TalentScout AI assistant. I'll be guiding you "
                f"through your screening today. I will collect some basic information "
                f"and ask a few technical questions.\n\n{DATA_PRIVACY_NOTICE}\n\n"
                f"To get started, what is your **full name**?")

    def get_progress_percentage(self) -> int:
        """Returns current progress (0-100) based on state machine."""
        return PROGRESS_MAP.get(self.stage, 0)

    def _call_llm(self, prompt: str, is_system_call: bool = True) -> str:
        """
        Wrapper for Groq API calls with error handling.
        
        Args:
            prompt (str): The prompt to send to the LLM.
            is_system_call (bool): Whether to inject the global SYSTEM_PROMPT.
        """
        messages = []
        if is_system_call:
            messages.append({"role": "system", "content": SYSTEM_PROMPT})
            
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return "I'm currently experiencing a brief technical connection issue. Could you please rephrase or try again?"

    def _handle_fallback(self, user_input: str) -> str:
        """Generates a dynamic fallback response for unclear inputs."""
        prompt = FALLBACK_PROMPT.format(stage=self.stage, message=user_input)
        return self._call_llm(prompt)

    def _extract_tech_stack(self, user_input: str) -> list[str]:
        """Extracts technologies from conversational input via LLM."""
        prompt = TECH_EXTRACTION_PROMPT.format(text=user_input)
        # Skip the main system prompt to keep the extraction focused strictly on the list
        response_text = self._call_llm(prompt, is_system_call=False)
        
        if "technical connection issue" in response_text:
            return []
            
        if "NONE" in response_text.upper():
            return []
        
        techs = [t.strip() for t in response_text.split(",") if t.strip()]
        return techs

    def _generate_technical_questions(self, technology: str) -> str:
        """Generates highly personalized questions based on tech, years, and role."""
        years = self.candidate_info.get("experience", "some")
        position = self.candidate_info.get("position", "Software Engineer")
        
        prompt = TECH_QUESTION_PROMPT.format(
            technology=technology, 
            years=years,
            position=position
        )
        return self._call_llm(prompt)

    def trigger_farewell(self) -> str:
        """Handles the final wrap-up, saves data, and sets terminal state."""
        self.stage = "FAREWELL"
        save_candidate(self.candidate_info, self.tech_stack, self.qa_pairs)
        return ("Thank you so much for your time! I have saved your profile and "
                "responses. The TalentScout team will review everything and reach "
                "out to you within 3–5 business days. Have a wonderful day!")

    def process_message(self, user_input: str) -> str:
        """Main state machine routing method."""
        clean_input = user_input.strip()
        
        # 1. Check Exit Keywords
        if clean_input.lower() in EXIT_KEYWORDS:
            return self.trigger_farewell()

        # 2. Empathy / Sentiment tracking (LLM tone is already adjusted in system prompt)
        sentiment_prefix = ""
        if detect_frustration(clean_input):
            sentiment_prefix = "I know technical interviews can be stressful, take a deep breath! You're doing great. "

        # 3. State Machine Routing
        response = ""
        
        if self.stage == "COLLECT_NAME":
            if len(clean_input) < 2:
                response = self._handle_fallback(clean_input)
            else:
                self.candidate_info["name"] = clean_input
                self.stage = "COLLECT_EMAIL"
                response = f"Nice to meet you, {clean_input}! What is your **email address**?"
                
        elif self.stage == "COLLECT_EMAIL":
            if validate_email(clean_input):
                self.candidate_info["email"] = clean_input
                self.stage = "COLLECT_PHONE"
                response = "Perfect. What is your **phone number**?"
            else:
                response = "That doesn't look like a valid email. Could you please provide a valid email address?"
                
        elif self.stage == "COLLECT_PHONE":
            if validate_phone(clean_input):
                self.candidate_info["phone"] = clean_input
                self.stage = "COLLECT_EXPERIENCE"
                response = "Great. How many **years of professional experience** do you have?"
            else:
                response = "Please provide a valid phone number (at least 10 digits)."
                
        elif self.stage == "COLLECT_EXPERIENCE":
            if validate_experience(clean_input):
                self.candidate_info["experience"] = clean_input
                self.stage = "COLLECT_POSITION"
                response = "Got it. What **job position** are you applying for?"
            else:
                response = "Please enter your experience as a number (e.g., 3 or 4.5)."
                
        elif self.stage == "COLLECT_POSITION":
            self.candidate_info["position"] = clean_input
            self.stage = "COLLECT_LOCATION"
            response = "Excellent. What is your current **city/location**?"
            
        elif self.stage == "COLLECT_LOCATION":
            self.candidate_info["location"] = clean_input
            self.stage = "COLLECT_TECH_STACK"
            response = ("Thanks! Now, please list **ALL the technologies** you are proficient in "
                        "(e.g., programming languages, frameworks, databases, cloud tools).")
                        
        elif self.stage == "COLLECT_TECH_STACK":
            techs = self._extract_tech_stack(clean_input)
            if not techs:
                response = "I couldn't detect specific technologies. Could you list them out clearly? (e.g., Python, React, SQL)"
            else:
                self.tech_stack = techs
                self.stage = "TECHNICAL_QUESTIONS"
                self.current_tech_index = 0
                
                first_tech = self.tech_stack[0]
                self.current_questions = self._generate_technical_questions(first_tech)
                response = (f"Impressive stack! Let's dive into some technical questions tailored for a {self.candidate_info.get('position')}.\n\n"
                            f"First up, **{first_tech}**:\n{self.current_questions}\n\n"
                            f"*Please answer all 3 questions in your next message.*")
                            
        elif self.stage == "TECHNICAL_QUESTIONS":
            current_tech = self.tech_stack[self.current_tech_index]
            
            self.qa_pairs.append({
                "technology": current_tech,
                "question": self.current_questions,
                "answer": clean_input
            })
            
            self.current_tech_index += 1
            if self.current_tech_index < len(self.tech_stack):
                next_tech = self.tech_stack[self.current_tech_index]
                self.current_questions = self._generate_technical_questions(next_tech)
                response = (f"Thank you. Next, let's talk about **{next_tech}**:\n"
                            f"{self.current_questions}\n\n"
                            f"*Please answer all 3 questions in your next message.*")
            else:
                return self.trigger_farewell()
                
        elif self.stage == "FAREWELL":
            response = "Your interview is complete! You can close this window. We will be in touch soon."

        return f"{sentiment_prefix}{response}"