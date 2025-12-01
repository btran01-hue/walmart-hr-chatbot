"""Test script to verify FAQ loading from docx file."""

import sys
import io
from knowledge_base import load_hr_knowledge_base, get_faq_document_path

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if __name__ == "__main__":
    print("Testing FAQ loading...\n")
    
    # Check FAQ path
    faq_path = get_faq_document_path()
    print(f"FAQ Document Path: {faq_path}")
    print(f"File exists: {faq_path.exists()}\n")
    
    # Load knowledge base
    print("Loading knowledge base...\n")
    kb = load_hr_knowledge_base()
    
    # Display results
    print("="*80)
    print("KNOWLEDGE BASE CONTENT:")
    print("="*80)
    print(kb)
    print("="*80)
    
    # Check if FAQ content is present
    if "Q:" in kb and "A:" in kb:
        print("\nSUCCESS! FAQ content loaded successfully!")
        
        # Count Q&A pairs
        q_count = kb.count("Q:")
        print(f"\nFound {q_count} questions in the FAQ")
    else:
        print("\nWARNING: FAQ content may not have loaded properly")
