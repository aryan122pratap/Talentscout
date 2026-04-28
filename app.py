"""Main Streamlit application file for TalentScout UI."""
import streamlit as st
from dotenv import load_dotenv

from chatbot import TalentScoutChatbot
from utils import format_interview_summary
from config import APP_NAME, APP_SUBTITLE

# Load environment variables
load_dotenv()

# Setup Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} | {APP_SUBTITLE}",
    page_icon="🎯",
    layout="centered"
)

# Custom CSS for Professional UI
st.markdown("""
<style>
    /* Chat window styling */
    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
    /* Logo Header */
    .header-container {
        display: flex;
        align-items: center;
        border-bottom: 2px solid #1E88E5;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .header-icon {
        font-size: 2.5rem;
        margin-right: 15px;
    }
    .header-text h1 {
        color: #1E88E5;
        margin: 0;
        padding: 0;
        font-size: 2rem;
    }
    .header-text p {
        color: #666;
        margin: 0;
        padding: 0;
        font-size: 1rem;
    }
    /* Progress bar branding */
    .stProgress > div > div > div > div {
        background-color: #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

def init_session():
    """Initializes standard session state variables."""
    if "bot" not in st.session_state:
        st.session_state.bot = TalentScoutChatbot()
        st.session_state.messages = []
        
        # Add Initial Greeting
        greeting = st.session_state.bot.get_initial_greeting()
        st.session_state.messages.append({"role": "assistant", "content": greeting})

def main():
    """Main Streamlit execution block."""
    init_session()
    bot: TalentScoutChatbot = st.session_state.bot

    # ---------------- HEADER ----------------
    st.markdown("""
    <div class="header-container">
        <div class="header-icon">🎯</div>
        <div class="header-text">
            <h1>TalentScout</h1>
            <p>AI Hiring Assistant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.title("🎯 TalentScout")
        
        # Progress Tracker
        st.subheader("Interview Progress")
        progress_val = bot.get_progress_percentage()
        st.progress(progress_val / 100.0)
        st.caption(f"Stage: {bot.stage.replace('_', ' ').title()}")
        
        # Candidate Info Summary
        st.subheader("Profile Summary")
        for key, val in bot.candidate_info.items():
            if val:
                st.write(f"**{key.title()}:** {val}")
                
        st.divider()
        
        # Export Button (Only valid if QAs exist)
        if len(bot.qa_pairs) > 0:
            summary_text = format_interview_summary(bot.candidate_info, bot.qa_pairs)
            st.download_button(
                label="📥 Download My Interview Summary",
                data=summary_text,
                file_name="TalentScout_Summary.txt",
                mime="text/plain",
                use_container_width=True
            )

        # Reset Button
        if st.button("🔄 Reset / Start Over", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # ---------------- CHAT WINDOW ----------------
    # Display message history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if bot.stage != "FAREWELL":
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            # Check previous stage to see if we advanced
            previous_stage = bot.stage
            
            # 1. Display User Message
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # 2. Get Bot Response
            with st.chat_message("assistant"):
                with st.spinner("TalentScout is thinking..."):
                    bot_response = bot.process_message(user_input)
                st.markdown(bot_response)
            
            # 3. Save Bot Message
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            # Interactive UI Element: Trigger a toast if the stage advanced
            if previous_stage != bot.stage and bot.stage != "FAREWELL":
                st.toast(f"✅ Saved! Moving to {bot.stage.replace('_', ' ').title()}", icon="💾")
                
            st.rerun()

if __name__ == "__main__":
    main()