# LAX2 HR Chatbot - Custom FAQ Reference

## ✅ Successfully Added FAQs

### 1. Leaving Before 5th Hour (Full Point)
**Keywords:** `5th hour`, `leave early full point`, `incomplete shift`

**Question Examples:**
- "If I leave before my 5th hour, is it a full point?"
- "What happens if I leave early before 5th hour?"

**Answer:** It will be a full point. Leaving prior to hitting your 5th hour is considered an incomplete shift therefore you will be receiving a full point. If you leave at your 5th hour or early prior to the end of your shift it will be 0.5.

---

### 2. Lunch Requirements at 6th Hour
**Keywords:** `6th hour`, `lunch exempt`, `skip lunch`

**Question Examples:**
- "If I leave at my 6th hour do I need to take lunch?"
- "Can I skip lunch if I leave at 6 hours?"

**Answer:** If you leave at your 6th hour or prior to your 6th hour you do not have to take a lunch.

---

### 3. Using PTO for Emergencies
**Keywords:** `pto emergency`, `pto vs ppto`, `use pto for emergency`

**Question Examples:**
- "Can I use PTO for an emergency?"
- "What's the difference between PTO and PPTO?"

**Answer:** No, PTO requires associates to submit the request for approval as far in advance. To cover emergencies, you must use PPTO.

---

### 4. No PPTO Available
**Keywords:** `no ppto`, `out of ppto`, `don't have ppto`

**Question Examples:**
- "What if I don't have PPTO?"
- "I'm out of PPTO, what happens?"

**Answer:** You risk obtaining an attendance point for Incomplete shift/ early out/ absence.

---

### 5. Medical Accommodations & Doctor Notes
**Keywords:** `doctor note accommodation`, `medical restriction`, `work restrictions`

**Question Examples:**
- "I have a doctor's note, can I work in a different area?"
- "How do I get medical accommodations?"

**Answer:** No, we cannot accommodate. You must go through the accommodation process and submit your doctor documentation to them to obtain approval. You would need to open a LOA to cover absences in the meantime you wait for confirmation approval from accommodations.

---

### 6. Leaving and Returning Same Shift
**Keywords:** `leave and come back`, `leave and return`

**Question Examples:**
- "Can I leave and come back during my shift?"
- "Can I go home and return?"

**Answer:** You must notify your manager prior to leaving the building however you are still responsible for covering your shift with PPTO for your need to leave early and come back.

---

### 7. Changing/Transferring Shifts
**Keywords:** `change shift`, `transfer shift`, `switch shift`

**Question Examples:**
- "How do I change my shift?"
- "Can I transfer to a different shift?"

**Answer:** To transfer you must review if we have open roles available and apply through the competitive process following with meeting time in position, attendance points and no orange-DA. If roles are not available, you will need to escalate your request through the Open-Door Process with an AGM and HRM.

---

### 8. Doctor's Note to Excuse Absence
**Keywords:** `doctor note excuse`, `doctors note absence`, `excuse with note`

**Question Examples:**
- "I brought a doctor's note, will it excuse my absence?"
- "Do you accept doctor's notes?"

**Answer:** Unfortunately, we do not take doctors' notes in house. You will either need to use PPTO, take the point or open an LOA with Sedgwick.

---

### 9. Calling Off When Using PPTO
**Keywords:** `call off ppto`, `call in with ppto`, `report absence ppto`

**Question Examples:**
- "Do I still have to call off if I use PPTO?"
- "Do I need to report my absence when using PPTO?"

**Answer:** Yes, if you do not call off when using PPTO, you may still receive an attendance point. You must report your absence through the Walmart associate hotline or Me@Walmart app, even when using PPTO to cover the time.

---

## 📝 How to Add More FAQs

1. Open: `C:\Users\btran\walmart-hr-chatbot\backend\knowledge_base.py`
2. Find the `FAQ_DATABASE = {` section
3. Add new entries before the closing `}`:

```python
"your_keyword": "Your exact answer here",
```

4. Restart the backend:
```batch
cd C:\Users\btran\walmart-hr-chatbot\backend
python main.py
```

## 🧪 Testing Your FAQs

1. Start the backend (if not running)
2. Open http://localhost:3000/chatbot.html
3. Type questions containing your keywords
4. Bot should respond with exact answers (95% confidence!)

---

**Created:** November 2025  
**Location:** LAX2 Walmart Distribution Center  
**Maintained by:** HR Team
