"""Simple HR Chatbot - Single File Version!

Just run: streamlit run simple_chatbot.py
"""

import streamlit as st
import os
from openai import OpenAI
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv("backend/.env")

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MICROSOFT_LIST_URL = os.getenv(
    "MICROSOFT_LIST_URL",
    "https://walmart.sharepoint.com/sites/HR/Lists/Resources"
)
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))

# FAQ Database
FAQ_DATABASE = {
    "pto": "Walmart associates earn PTO (Paid Time Off) based on their tenure and position. Full-time associates typically earn more PTO than part-time associates. You can check your PTO balance on the WalmartOne portal or the Me@Walmart app.",
    "benefits": "Walmart offers comprehensive benefits including health insurance, dental, vision, 401k with company match, associate discount, and more. Eligibility depends on your employment status (full-time/part-time) and tenure.",
    "pay_schedule": "Walmart associates are typically paid bi-weekly on Thursdays. You can set up direct deposit through the WalmartOne portal.",
    "discount": "Walmart associates receive a 10% discount on regularly priced general merchandise and fresh produce at Walmart stores. The discount card can be used immediately after activation.",
    "live_better_u": "Live Better U is Walmart's education benefit program offering associates the opportunity to earn a degree or learn new skills with tuition, books, and fees paid for by Walmart. Programs include high school completion, college degrees, and skills training.",
}

SYSTEM_PROMPT = """You are an HR assistant chatbot for Walmart associates. Your role is to help answer common HR-related questions.

Common Topics:
1. Benefits & Insurance - Health insurance, 401k, PTO, associate discount
2. Payroll & Compensation - Pay schedules, direct deposit, W2 forms, overtime
3. Leave Policies - Medical leave (FMLA), parental leave, bereavement, jury duty
4. Career Development - Internal jobs, training, tuition assistance, performance reviews
5. Workplace Policies - Dress code, attendance, code of conduct

Guidelines:
- Be professional, friendly, and empathetic
- Provide accurate information based on Walmart policies
- If you're unsure, acknowledge it
- Keep responses concise (2-3 paragraphs maximum)
- Use simple, clear language
- Always prioritize associate well-being
"""

# Initialize OpenAI client
if OPENAI_API_KEY and OPENAI_API_KEY != "sk-proj-paste-your-new-key-here":
    client = OpenAI(api_key=OPENAI_API_KEY)
    AI_ENABLED = True
else:
    AI_ENABLED = False


def search_faq(query: str) -> str | None:
    """Search FAQ database for quick answers."""
    query_lower = query.lower()
    for keyword, answer in FAQ_DATABASE.items():
        if keyword in query_lower:
            return answer
    return None


def calculate_confidence(response: str, query: str) -> float:
    """Calculate confidence score."""
    uncertainty_phrases = [
        "i'm not sure", "i don't know", "unclear",
        "cannot confirm", "recommend contacting",
        "please contact", "check with hr",
    ]
    
    response_lower = response.lower()
    if any(phrase in response_lower for phrase in uncertainty_phrases):
        return 0.5
    if len(response.split()) < 10:
        return 0.6
    if search_faq(query):
        return 0.95
    return 0.8


def get_response(message: str, chat_history: list) -> tuple[str, float, bool]:
    """Get chatbot response.
    
    Returns:
        (response_text, confidence, show_fallback)
    """
    # Check FAQ first
    faq_answer = search_faq(message)
    if faq_answer:
        return faq_answer, 0.95, False
    
    # If AI is not enabled, return fallback
    if not AI_ENABLED:
        return (
            "I don't have a specific answer for that question. Please check the HR resources for more information.",
            0.0,
            True
        )
    
    try:
        # Build messages for OpenAI
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(chat_history[-10:])  # Last 10 messages
        messages.append({"role": "user", "content": message})
        
        # Call OpenAI
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        
        answer = response.choices[0].message.content
        confidence = calculate_confidence(answer, message)
        show_fallback = confidence < CONFIDENCE_THRESHOLD
        
        return answer, confidence, show_fallback
        
    except Exception as e:
        return (
            f"I'm having trouble right now. Please check the HR resources list for assistance. (Error: {str(e)})",
            0.0,
            True
        )


# Streamlit UI
st.set_page_config(
    page_title="Walmart HR Assistant",
    page_icon="💼",
    layout="centered"
)

# Header
st.title("💼 Walmart HR Assistant")
st.caption("Your 24/7 HR support companion")

# API Key Check
if not AI_ENABLED:
    st.warning("⚠️ OpenAI API key not configured. Only FAQ answers will work. Edit `backend/.env` to add your API key.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.show_fallback = False

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(message["timestamp"])

# Display fallback banner if needed
if st.session_state.show_fallback:
    st.info(
        f"ℹ️ **Need more specific information?**\n\n"
        f"I'm not entirely certain about this answer. For the most accurate and up-to-date information, "
        f"please check our [HR Resources]({MICROSOFT_LIST_URL}).",
        icon="ℹ️"
    )

# Chat input
if prompt := st.chat_input("Ask me about benefits, PTO, payroll, or other HR topics..."):
    # Add user message to chat
    timestamp = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text, confidence, show_fallback = get_response(
                prompt,
                st.session_state.chat_history
            )
        
        st.markdown(response_text)
        timestamp = datetime.now().strftime("%I:%M %p")
        st.caption(f"{timestamp} • Confidence: {confidence:.0%}")
    
    # Add assistant message to chat
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "timestamp": timestamp
    })
    
    # Update chat history for OpenAI
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
    
    # Update fallback state
    st.session_state.show_fallback = show_fallback
    
    # Rerun to show fallback banner
    if show_fallback:
        st.rerun()

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This chatbot helps Walmart associates with HR questions.
    
    **Features:**
    - Instant FAQ answers
    - AI-powered responses
    - Microsoft List fallback
    
    **Common Topics:**
    - Benefits & Insurance
    - PTO & Leave Policies
    - Payroll & Compensation
    - Career Development
    
    **Try asking:**
    - "What is PTO?"
    - "How do I check my benefits?"
    - "Tell me about Live Better U"
    """)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.show_fallback = False
        st.rerun()
    
    st.divider()
    st.caption("💙 Built for Walmart Associates")
