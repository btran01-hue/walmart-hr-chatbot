"""Simple one-question test of the chatbot."""

import requests
import json
import sys
import io

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BACKEND_URL = "http://127.0.0.1:8000"

def test_faq_question():
    """Test a simple FAQ question."""
    question = "If I leave before my 5th hour, will it be half a point or full point?"
    
    print(f"Testing chatbot with FAQ question:")
    print(f"Q: {question}\n")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json={
                "message": question,
                "conversation_history": []
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"CHATBOT RESPONSE:")
            print(f"{data['response']}")
            print(f"\nMetadata:")
            print(f"  - Confidence: {data['confidence']:.2%}")
            print(f"  - Show Fallback: {data['show_fallback']}")
            if data.get('sources'):
                print(f"  - Sources: {', '.join(data['sources'])}")
            
            # Check if the answer is correct based on FAQ
            expected_keywords = ["full point", "5th hour", "incomplete shift", "0.5"]
            answer_lower = data['response'].lower()
            
            if any(keyword.lower() in answer_lower for keyword in expected_keywords):
                print("\nSUCCESS! The chatbot referenced the FAQ correctly!")
            else:
                print("\nWARNING: The answer doesn't seem to reference the FAQ...")
                
        else:
            print(f"ERROR: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend.")
        print("Make sure the backend is running: cd walmart-hr-chatbot/backend && uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("="*80)
    print("WALMART HR CHATBOT - FAQ TEST")
    print("="*80)
    print()
    
    success = test_faq_question()
    
    print()
    print("="*80)
    
    sys.exit(0 if success else 1)
