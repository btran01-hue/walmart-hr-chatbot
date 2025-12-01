# LAX2 HR Chatbot - Fallback Configuration Update

## ✅ What Was Changed

Updated the chatbot to direct associates to submit requests to the LAX2 HR SharePoint list when the chatbot cannot answer their question.

---

## 🔗 SharePoint List URL

**LAX2 HR Request Submission Form:**
```
https://teams.wal-mart.com/sites/LAX2HR560/_layouts/15/listforms.aspx?cid=NjBiN2EyYmQtZjNlZC00MTk1LTkyMDUtMTZiMzU0MWY2OWM4&nav=NTIwMTZjNDEtNDhjNi00MTFhLThjN2MtNTY0YjRjM2Q0NTE5
```

---

## 📝 Files Updated

### 1. **Backend Configuration** (.env)
**File:** `C:\Users\btran\walmart-hr-chatbot\backend\.env`

**Changed:**
```env
# OLD:
MICROSOFT_LIST_URL=https://walmart.sharepoint.com/sites/HR/Lists/Resources

# NEW:
MICROSOFT_LIST_URL=https://teams.wal-mart.com/sites/LAX2HR560/_layouts/15/listforms.aspx?cid=NjBiN2EyYmQtZjNlZC00MTk1LTkyMDUtMTZiMzU0MWY2OWM4&nav=NTIwMTZjNDEtNDhjNi00MTFhLThjN2MtNTY0YjRjM2Q0NTE5
```

---

### 2. **Error Message** (chatbot_service.py)
**File:** `C:\Users\btran\walmart-hr-chatbot\backend\chatbot_service.py`

**Changed:**
```python
# OLD:
response="I'm having trouble processing your request right now. Please check the HR resources list for assistance."

# NEW:
response="I'm having trouble processing your request right now. Please submit your question to the LAX2 HR team using the link below, and they will respond to you as soon as possible."
```

---

### 3. **Fallback Banner** (chatbot.html)
**File:** `C:\Users\btran\walmart-hr-chatbot\chatbot.html`

**Changed:**
```html
<!-- OLD: -->
<strong>ℹ️ Need more specific information?</strong><br>
I'm not entirely certain about this answer. For the most accurate information, 
please check the <a href="${url}" target="_blank">HR Resources List</a>.

<!-- NEW: -->
<strong>📝 Can't find what you're looking for?</strong><br>
I'm not entirely certain about this answer. Please submit your question to the LAX2 HR team by 
<a href="${url}" target="_blank"><strong>clicking here to submit a request</strong></a>. 
They will respond to you as soon as possible!
```

---

### 4. **System Prompt** (knowledge_base.py)
**File:** `C:\Users\btran\walmart-hr-chatbot\backend\knowledge_base.py`

**Changed:**
```python
# OLD:
"When you cannot provide a definitive answer:
- Acknowledge the question
- Explain why you cannot provide a specific answer
- Suggest the associate check the Microsoft List or contact HR directly"

# NEW:
"When you cannot provide a definitive answer:
- Acknowledge the question
- Explain why you cannot provide a specific answer
- Direct the associate to submit their request to the LAX2 HR team through the SharePoint list
- Encourage them that the HR team will respond as soon as possible
- Be encouraging and helpful, not dismissive"
```

---

## 🚀 How It Works Now

### **Scenario 1: Low Confidence Answer**
When the chatbot's confidence is below 70% (CONFIDENCE_THRESHOLD):

1. ✅ Chatbot provides its best answer
2. 🟡 Shows yellow fallback banner
3. 🔗 Banner links to LAX2 HR SharePoint request form
4. 📝 Associates can submit their question for HR team to answer

**Example:**
```
Associate: "Can I get tuition reimbursement for coding bootcamp?"

Chatbot: "Walmart offers tuition assistance through Live Better U..."
[Confidence: 65%]

📝 Can't find what you're looking for?
I'm not entirely certain about this answer. Please submit your 
question to the LAX2 HR team by clicking here to submit a request. 
They will respond to you as soon as possible!
```

---

### **Scenario 2: Error/No Answer**
When the chatbot encounters an error or can't answer:

1. ❌ Shows error message
2. 🔗 Directs to SharePoint submission form
3. 📝 HR team gets the question

**Example:**
```
Chatbot: "I'm having trouble processing your request right now. 
Please submit your question to the LAX2 HR team using the link 
below, and they will respond to you as soon as possible."

📝 Can't find what you're looking for?
[Click here to submit a request]
```

---

## ⚙️ Configuration Settings

**Confidence Threshold:** 0.7 (70%)
- Answers below 70% confidence will show the fallback banner
- Answers above 70% confidence will not show the banner

**To adjust confidence threshold:**
Edit `.env` file:
```env
CONFIDENCE_THRESHOLD=0.7  # Change to 0.6 for more lenient, 0.8 for stricter
```

---

## 🔄 Next Steps: Restart Backend

For these changes to take effect:

```batch
cd C:\Users\btran\walmart-hr-chatbot\backend
python main.py
```

Or if using uvicorn:
```batch
cd C:\Users\btran\walmart-hr-chatbot\backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 Testing the Fallback

### **Test 1: Ask an unknown question**
```
Associate: "What's the weather tomorrow?"
→ Should show fallback banner with SharePoint link
```

### **Test 2: Ask a complex policy question**
```
Associate: "Can I transfer to a different FC in another state?"
→ Chatbot may answer but show fallback if unsure
```

### **Test 3: Ask a FAQ question**
```
Associate: "If I leave before my 5th hour is it a full point?"
→ Should answer confidently (95%) with NO fallback banner
```

---

## 📊 Expected Behavior

| Question Type | Confidence | Shows Fallback? | Links to SharePoint? |
|--------------|-----------|----------------|---------------------|
| FAQ Match (exact) | 95% | ❌ No | ❌ No |
| AI Answer (high confidence) | 80-90% | ❌ No | ❌ No |
| AI Answer (medium confidence) | 60-70% | ✅ Yes | ✅ Yes |
| AI Answer (low confidence) | <60% | ✅ Yes | ✅ Yes |
| Error/Unknown | 0% | ✅ Yes | ✅ Yes |

---

**Updated:** November 2025  
**Location:** LAX2 Walmart Distribution Center  
**Maintained by:** HR Team
