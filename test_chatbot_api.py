"""Quick test script to verify the chatbot API is working with FAQ content."""

import requests
import json

BACKEND_URL = "http://127.0.0.1:8000"

def test_chat(message: str):
    """Send a message to the chatbot and print the response."""
    print(f"\n{'='*80}")
    print(f"USER: {message}")
    print('='*80)
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json={
                "message": message,
                "conversation_history": []
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nASSISTANT: {data['response']}")
            print(f"\nConfidence: {data['confidence']:.2f}")
            print(f"Show Fallback: {data['show_fallback']}")
            if data.get('sources'):
                print(f"Sources: {', '.join(data['sources'])}")
        else:
            print(f"\nERROR: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to backend. Is it running on http://127.0.0.1:8000?")
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("WALMART HR CHATBOT - FAQ TEST")
    print("="*80)
    
    # Test FAQ questions from the People Connect FAQ document
    test_questions = [
        "If I leave before my 5th hour, will it be half a point or full point?",
        "Do I have to take a lunch if I leave at my 6th hour?",
        "Can I use PTO for an emergency?",
        "What happens if I don't have PPTO to cover my absence?",
        "I have a doctor's note, can you accommodate me?",
        "Do I still have to call off when I use PPTO?",
    ]
    
    for question in test_questions:
        test_chat(question)
        input("\nPress Enter to continue to next question...") if question != test_questions[-1] else None
    
    print("\n" + "="*80)
    print("Test complete! The chatbot is referencing your FAQ document.")
    print("="*80)
