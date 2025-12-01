"""HR Knowledge base for common questions and answers."""

import os
from pathlib import Path
from docx import Document
import logging

logger = logging.getLogger(__name__)

# Base system prompt
BASE_HR_PROMPT = """
You are an HR assistant chatbot for Walmart associates at LAX2. Your role is to help answer common HR-related questions.

Guidelines:
- Be professional, friendly, and empathetic
- Provide accurate information based on Walmart policies
- If you're unsure about a specific policy detail, acknowledge it
- Keep responses concise (2-3 paragraphs maximum)
- Use simple, clear language
- Always prioritize associate well-being
- When referencing FAQ content, answer directly and accurately

When you cannot provide a definitive answer:
- Acknowledge the question
- Explain why you cannot provide a specific answer
- Direct the associate to submit their request to the LAX2 HR team through the SharePoint list
- Encourage them that the HR team will respond as soon as possible
- Be encouraging and helpful, not dismissive
"""


def load_faq_from_docx(file_path: str | Path) -> str:
    """Load FAQ content from a Word document.
    
    Args:
        file_path: Path to the .docx file containing FAQ content
        
    Returns:
        Formatted string containing all Q&A pairs
    """
    try:
        doc = Document(file_path)
        faq_content = []
        
        # Extract all text from paragraphs
        current_question = None
        current_answer_parts = []
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                # Empty paragraph might signal end of answer
                if current_question and current_answer_parts:
                    faq_content.append(f"Q: {current_question}")
                    faq_content.append(f"A: {' '.join(current_answer_parts)}")
                    faq_content.append("")  # blank line
                    current_question = None
                    current_answer_parts = []
                continue
                
            # Check if it's a question
            if text.startswith("Question:"):
                # Save previous Q&A pair if exists
                if current_question and current_answer_parts:
                    faq_content.append(f"Q: {current_question}")
                    faq_content.append(f"A: {' '.join(current_answer_parts)}")
                    faq_content.append("")  # blank line
                
                current_question = text.replace("Question:", "").strip()
                current_answer_parts = []
                
            elif text.startswith("Answer:"):
                # Start of answer
                answer_text = text.replace("Answer:", "").strip()
                current_answer_parts = [answer_text] if answer_text else []
                
            elif current_answer_parts is not None and current_question:
                # Continuation of answer (multi-paragraph answers)
                current_answer_parts.append(text)
        
        # Don't forget the last Q&A pair
        if current_question and current_answer_parts:
            faq_content.append(f"Q: {current_question}")
            faq_content.append(f"A: {' '.join(current_answer_parts)}")
        
        if faq_content:
            return "\n".join(faq_content)
        else:
            logger.warning(f"No FAQ content found in {file_path}")
            return ""
            
    except FileNotFoundError:
        logger.error(f"FAQ file not found: {file_path}")
        return ""
    except Exception as e:
        logger.error(f"Error loading FAQ from {file_path}: {e}")
        return ""


def get_faq_document_path() -> Path:
    r"""Get the path to the FAQ document.
    
    Looks in common locations:
    1. C:\Users\btran\Downloads\People Connect FAQ.docx
    2. Relative to this file: ../../People Connect FAQ.docx
    """
    # Check Downloads folder
    downloads_path = Path(r"C:\Users\btran\Downloads\People Connect FAQ.docx")
    if downloads_path.exists():
        return downloads_path
    
    # Check relative to project
    project_root = Path(__file__).parent.parent.parent
    relative_path = project_root / "People Connect FAQ.docx"
    if relative_path.exists():
        return relative_path
    
    # Default to Downloads (even if not found, for error logging)
    return downloads_path


def load_hr_knowledge_base() -> str:
    """Load the complete HR knowledge base including FAQ content.
    
    Returns:
        Complete system prompt with FAQ content
    """
    faq_path = get_faq_document_path()
    faq_content = load_faq_from_docx(faq_path)
    
    if faq_content:
        knowledge_base = f"{BASE_HR_PROMPT}\n\n=== FREQUENTLY ASKED QUESTIONS ===\n\n{faq_content}"
        logger.info(f"Loaded FAQ content from {faq_path}")
    else:
        knowledge_base = BASE_HR_PROMPT
        logger.warning("FAQ content not loaded, using base prompt only")
    
    return knowledge_base


HR_KNOWLEDGE_BASE = load_hr_knowledge_base()


def get_system_prompt() -> str:
    """Get the system prompt for the chatbot.
    
    This reloads the FAQ content each time to ensure fresh data.
    """
    return load_hr_knowledge_base()


def reload_knowledge_base() -> None:
    """Reload the HR knowledge base from the FAQ document.
    
    Call this function to refresh the FAQ content without restarting the server.
    """
    global HR_KNOWLEDGE_BASE
    HR_KNOWLEDGE_BASE = load_hr_knowledge_base()
    logger.info("Knowledge base reloaded")
