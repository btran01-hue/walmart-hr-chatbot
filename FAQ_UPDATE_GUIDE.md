# FAQ Update Guide

## Overview

Your chatbot now **automatically loads FAQ content** from the Word document:
```
C:\Users\btran\Downloads\People Connect FAQ.docx
```

## How It Works

1. **Automatic Loading**: When the chatbot starts, it reads the FAQ document and includes all Q&A pairs in the AI's knowledge base
2. **No Code Changes Needed**: Just update the Word document, and restart the chatbot to see changes
3. **Structured Format**: The document uses "Question:" and "Answer:" prefixes which the system automatically parses

## Current FAQ Content

The chatbot currently has **9 FAQ questions** loaded, including:
- Points for leaving before/after 5th hour
- Lunch requirements at 6th hour
- PTO vs PPTO for emergencies
- Medical accommodations process
- Shift changes and transfers
- Doctor's note policies
- Call-off procedures when using PPTO

## Updating the FAQ

### Option 1: Edit the Existing Document

1. Open `C:\Users\btran\Downloads\People Connect FAQ.docx`
2. Add/edit questions following this format:
   ```
   Question: [Your question here]?
   Answer: [Your answer here]
   ```
3. Save the document
4. Restart the chatbot (the backend will reload the FAQ automatically)

### Option 2: Move the Document

If you want to move the FAQ document to a different location:

1. Update the path in `backend/knowledge_base.py` in the `get_faq_document_path()` function
2. Or copy the FAQ document to the project root as `People Connect FAQ.docx`

## Testing FAQ Loading

To verify the FAQ is loading correctly:

```bash
cd walmart-hr-chatbot/backend
python test_faq_loading.py
```

This will show:
- FAQ document location
- Whether the file exists
- All loaded Q&A pairs
- Number of questions found

## How Associates Use It

1. Associates ask questions in the chat interface
2. The AI reads the system prompt which includes all FAQ content
3. The AI answers based on the FAQ when possible
4. If the AI can't answer with certainty, it directs them to submit via SharePoint

## Important Notes

- **Restart Required**: Changes to the FAQ document require a backend restart to take effect
- **Format Matters**: Keep the "Question:" and "Answer:" format for proper parsing
- **Incomplete Answers**: The last FAQ answer in your current document appears truncated - you may want to complete it:
  ```
  Question: Do I still have to call off when i put PPTO?
  Answer: Yes, if you do [complete this answer]
  ```

## Troubleshooting

**FAQ not loading?**
1. Check the file path is correct
2. Ensure `python-docx` is installed: `uv pip install python-docx`
3. Run the test script to see detailed error messages
4. Check backend logs when starting the server

**Questions not being answered correctly?**
1. Verify the FAQ content with the test script
2. Make sure questions are clearly phrased in the document
3. Ensure answers are complete and accurate

## Next Steps

To make the chatbot more useful:

1. **Complete the last FAQ answer** about calling off with PPTO
2. **Add more questions** that associates frequently ask
3. **Test with real questions** to see how well the AI references the FAQ
4. **Share with the team** and gather feedback on what FAQs to add

---

**Note**: The FAQ document is the single source of truth for HR questions. Keep it updated and the chatbot will automatically have the latest information!
