# 🎯 TalentScout: AI-Powered Recruitment Assistant

> A production-grade, conversational AI screening agent designed for modern recruitment agencies — fast, personalized, and context-aware.

## 📖 Project Overview

**TalentScout** is an intelligent hiring assistant chatbot built for **TalentScout**, a fictional recruitment agency specializing in technology placements. It automates the initial candidate screening process by conducting structured, conversational interviews powered by a large language model.

The assistant collects essential candidate information, detects their tech stack from natural language, and dynamically generates tailored technical interview questions — all within a polished, professional Streamlit interface.

Built on a **strict state-machine architecture** and powered by the **Groq LPU Inference Engine**, TalentScout delivers near-zero latency responses while maintaining a coherent, human-like interview experience from greeting to farewell.

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| ⚡ **Near-Zero Latency** | Leverages Groq's LPU architecture with `llama-3.3-70b-versatile` for instantaneous responses |
| 🏗️ **Strict State Machine** | Candidates can never skip stages; all PII is validated before the technical assessment begins |
| 🌍 **Native Multilingual Support** | Detects and matches the candidate's language (Hindi, Spanish, French, etc.) in real-time |
| 🧬 **Hyper-Personalized Q&A** | Technical questions are generated based on specific tech stack, years of experience, and desired role |
| ❤️ **Empathy & Sentiment Engine** | Detects candidate frustration and triggers supportive, encouraging responses |
| 🔐 **GDPR & Privacy Focused** | Mandatory privacy notice, validated PII collection, and anonymization utilities |
| 📥 **Interview Export** | Candidates can download a formatted `.txt` summary of their full interview and responses |
| 🎨 **Custom UI** | Dark-themed, professional Streamlit interface with custom CSS, chat bubbles, and sidebar tracker |

---

## 🛠️ Technical Stack

| Category | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Interface** | Streamlit (Custom CSS & Interactive Toasts) |
| **Inference Engine** | Groq Cloud |
| **LLM Model** | Meta LLaMA 3.3 70B Versatile |
| **Data Storage** | Persistent Local JSON |
| **Environment** | Python-Dotenv |

---

## 📂 Project Architecture

```
talentscout/
├── app.py              # Streamlit UI, Session State & Interactive Elements
├── chatbot.py          # Core Logic, State Machine & Groq Integration
├── config.py           # Global Constants, Model Config & Stage Mapping
├── prompts.py          # System Instructions & Dynamic Prompt Templates
├── utils.py            # Regex Validation, Sentiment Analysis & Formatting Helpers
├── data_handler.py     # GDPR Privacy Notice & Local JSON Storage Logic
├── requirements.txt    # Project Dependencies
├── .env.example        # Environment Variable Template
└── README.md           # Project Documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- A free [Groq API Key](https://console.groq.com)
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/talentscout.git
cd talentscout
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory by copying the example:

```bash
cp .env.example .env
```

Then open `.env` and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

> Get a free API key at [console.groq.com](https://console.groq.com) — no credit card required.

### 5. Launch the Application

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 🧭 Usage Guide

1. **Open the app** in your browser at `http://localhost:8501`
2. **Read the privacy notice** displayed at the start of the session
3. **Answer each question** one at a time — the bot collects your name, email, phone, experience, desired position, location, and tech stack
4. **Declare your tech stack** freely — e.g., *"Python, Django, PostgreSQL, Docker, AWS"*
5. **Answer the technical questions** — 3 targeted questions are generated per technology
6. **Download your interview summary** using the button in the sidebar when the session ends
7. **Start over** at any time using the "Reset / Start Over" button

---

## 🧠 Technical Implementation Details

### Dynamic Prompting Strategy

TalentScout uses a **multi-layered prompting strategy** to ensure professional boundaries and high-quality output:

- **The System Firewall**: A strict system prompt prevents the LLM from answering off-topic questions, providing coding help, or revealing internal model details. If a candidate goes off-topic, the bot politely redirects them back to the interview.

- **Tech Extraction Layer**: A specialized "logic-only" LLM call parses free-form candidate input (e.g., *"I know Python, a bit of React, and some AWS"*) into a clean structured list (`["Python", "React", "AWS"]`) — without any conversational fluff in the output.

- **Role-Based Personalization**: The candidate's target job title and years of experience are injected into the interviewer prompt. A candidate applying for a *"Senior Backend Engineer"* with 8 years of experience receives significantly harder questions than one applying for an *"Intern"* role with 1 year of experience.

- **Fallback Handling**: When input is ambiguous or unclear, a dedicated fallback prompt acknowledges the candidate's message and smoothly redirects them to the current interview stage.

### State Machine Logic

The conversation flows through a strict, linear state machine. No stage can be skipped:

```
GREETING → COLLECT_NAME → COLLECT_EMAIL → COLLECT_PHONE
    → COLLECT_EXPERIENCE → COLLECT_POSITION → COLLECT_LOCATION
        → COLLECT_TECH_STACK → TECHNICAL_QUESTIONS → FAREWELL
```

Each stage has a dedicated handler that validates input, stores it in session state, and advances the stage only upon successful validation.

### Sentiment Analysis

A lightweight keyword-based sentiment engine in `utils.py` scans each user message for signals of frustration or confusion (e.g., *"I don't know"*, *"I'm confused"*, *"this is hard"*). When detected, the bot acknowledges the feeling and responds with an extra layer of encouragement before continuing.

---

## 🛡️ Data Privacy & Security

TalentScout is designed with data privacy as a first-class concern:

- **Transparency**: A mandatory GDPR-aligned privacy notice is displayed at the start of every session, informing candidates what data is collected, why, and how it is stored.
- **Input Validation**: Phone numbers and email addresses are validated using standard regex patterns *before* the interview proceeds, ensuring data integrity.
- **Secure Local Storage**: All candidate data is saved to a local `candidates_data.json` file. No data is sent to any third-party service other than the Groq inference API for LLM calls.
- **PII Anonymization**: `data_handler.py` includes an `anonymize_candidate()` utility that masks email addresses and phone numbers when exporting or sharing data logs.
- **No Data Selling**: Candidate data is strictly used for recruitment screening purposes and is never shared with advertisers or third parties.

---

## 🤝 Challenges & Solutions

**Challenge 1: Parsing Free-Form Tech Stack Input**

Candidates describe their skills in highly varied ways — *"I mainly use Python, know a bit of React and have worked with AWS S3"*. A simple split-by-comma approach would fail.

**Solution**: A dedicated LLM call with a logic-only prompt extracts a clean, normalized list of technologies. The prompt explicitly instructs the model to return only a JSON array with no extra text, which is then safely parsed.

---

**Challenge 2: Maintaining Strict Conversation Context**

Without careful state management, the LLM could get confused about what stage the conversation is in, especially over long sessions.

**Solution**: The state machine in `chatbot.py` fully controls conversation flow in Python. The LLM is only called for NLG (natural language generation) — it never decides what the *next* stage is. Stage transitions are handled entirely by deterministic Python logic.

---

**Challenge 3: Preventing Prompt Injection & Off-Topic Responses**

Candidates might attempt to get the bot to answer coding questions, reveal its model, or go off-topic.

**Solution**: A strict system prompt acts as a firewall, explicitly listing prohibited behaviors. Additionally, all user inputs are routed through stage-specific handlers rather than a generic LLM call, making prompt injection attempts largely ineffective.

---

**Challenge 4: Validating PII Without Frustrating Users**

Rejecting invalid emails or phone numbers harshly can frustrate candidates and hurt the experience.

**Solution**: Validation failures trigger warm, encouraging re-prompts rather than blunt error messages. The bot explains what format is expected and gives the candidate another chance without judgment.

---

## 🔮 Future Improvements

- **☁️ Cloud Deployment**: Deploy on Streamlit Community Cloud or GCP Cloud Run with environment secrets management for a live, shareable demo link
- **🗄️ Database Backend**: Replace local JSON with a PostgreSQL or Firebase database for multi-user, concurrent session support
- **📊 Recruiter Dashboard**: A separate admin panel to review all candidate submissions, filter by tech stack, and export reports
- **🎙️ Voice Interface**: Integrate speech-to-text (Whisper API) so candidates can speak their answers
- **📧 Auto Email Notifications**: Send a confirmation email to candidates and a summary email to recruiters upon interview completion
- **🔄 Resume Parsing**: Allow candidates to upload a PDF resume and auto-populate their information and tech stack

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Built as part of the **TalentScout AI/ML Intern Assignment**.

---

*TalentScout — Screening smarter, not harder.* 🎯
