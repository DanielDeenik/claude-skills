# Evening Cycle — Full Operational Playbook (v2 — ACTION-FIRST)

Run at 21:00 Amsterdam time. Aligned with Dan's wind-down period (21:30 Goddard night seed,
22:00 sleep). Must complete by 21:25 so Dan can read the review.

**v2 CHANGE: The evening cycle now CLEANS before it reviews. Phase 2 is active email
archiving + file sweep, not just "check if things are dirty."**

---

## Phase 1: REVIEW — What Happened Today

### Email Activity Summary

1. Use `gmail_search_messages` to pull today's emails:
   - `after:YYYY/MM/DD before:YYYY/MM/DD+1` for received
   - `in:sent after:YYYY/MM/DD` for sent
   - `is:unread` for current unread count
2. Count: messages received, messages sent/replied
3. Flag anything that slipped through — unread from real humans, payment issues

### File Activity Summary

1. Scan workspace for files modified today
2. Note what was created, moved, or changed
3. Check Downloads/Desktop state (screenshot via computer-use if available)

### Calendar Review

1. `gcal_list_events` for today — note completed vs. missed/cancelled
2. Capture action items from meetings

### Win Detection

Scan for wins — frame through identity: "The man who..." not "I managed to..."

---

## Phase 2: CLEAN — Evening Email + File Pass (NEW in v2)

**This is the critical upgrade. The evening cycle now actively cleans, not just reviews.**

### Email Cleanup via Chrome MCP

1. Navigate to Gmail in Chrome
2. Run the same batch definitions from SKILL.md against today's accumulated email:

   **Quick batches (< 5 min total):**
   - Newsletters received today that weren't caught by morning cycle → label + archive
   - Receipts/confirmations from today → label + archive
   - Promotions accumulated during the day → archive
   - Consulting emails (non-money) → label + archive

3. Search `is:unread` — count what remains. Goal: under 5 unread, all of them
   requiring Dan's personal attention.

4. For any email that needs a reply Dan hasn't sent, create a draft via `gmail_create_draft`
   with a suggested response. Note it in the brief.

### File Sweep

If computer-use is available:
1. Screenshot Desktop — if files appeared during the day, route them now
2. Screenshot Downloads — route any new files
3. Verify Desktop is clean
4. Goal: Dan wakes to a clean slate

If no screen access:
1. Note that file sweep was skipped
2. Include in morning cycle queue

### Record Cleanup Metrics

- Emails archived in evening pass
- Emails remaining unread (with subjects)
- Files moved (if any)
- Desktop status: clean / needs attention

---

## Phase 3: PREP — Load Tomorrow

### Flow Block Planning (most important part)

Napoleon Hill: "The person of decision cannot be stopped."

1. **Flow Block 1 (05:32-08:30):** THE most important task.
   - Must be creative/generative (not admin — admin is already handled by autopilot)
   - Must serve the Definite Chief Aim
   - Must be specific enough to start in 90 seconds
   - Write as: "Open [specific file/tool] and [specific first action]"

2. **Flow Block 2 (10:00-13:00):** Second-priority deep work.
   - More structured/analytical
   - Complements Block 1

3. **Flow Block 3 (14:30-17:30):** Third-priority work or learning.

### Calendar Preview

1. `gcal_list_events` for tomorrow
2. Flag conflicts with flow blocks
3. Note prep needed
4. Is tomorrow's calendar protecting deep work time?
   - If not, consider using `gcal_create_event` to block focus time

### Open Loop Capture

List everything unresolved. Writing them releases them from the mind (GTD + Hill):
- Unanswered emails requiring attention
- Tasks started but not completed
- Commitments from meetings
- Items from morning brief not addressed

---

## Phase 4: SEED — Goddard Night Programming

### Select Tomorrow's Affirmation

Based on tomorrow's day of week:
- Monday → €50,000/month income
- Tuesday → €1M angel investments deployed
- Wednesday → Free from consulting
- Thursday → 72kg vital body
- Friday → Living in Mallorca
- Saturday → Happy Money Project
- Sunday → Integration + gratitude

### Generate the Night Seed

Write a first-person, present-tense visualization (3-5 sentences):
1. Goal stated as ALREADY ACHIEVED (never "I will" — only "I am" / "I have")
2. Sensory detail (what Dan sees, hears, feels)
3. Emotional tone (gratitude, calm confidence, joy)
4. Reference real current progress where possible
5. Short enough to hold in mind while falling asleep

### Singer Integration

One-line release prompt: "Notice [specific tension from today]. Let it pass through. You are not that."

---

## Phase 5: BRIEF — Generate Evening Review

Compile into the Evening Review format from SKILL.md.

**Key change from v1:** The brief now includes ACTIONS TAKEN (emails archived, files moved)
alongside the review and prep sections. Dan sees what was cleaned, not what needs cleaning.

**Delivery:** Apple Notes + workspace markdown file (`Reports/evening-review-YYYY-MM-DD.md`)

**Tone:** Warm, grounding, supportive. No stress, no guilt. Open loops are opportunities.
This is the last thing Dan reads before Goddard practice.

**Timing:** Complete by 21:25. Dan reads review, then 21:30 Goddard, then 22:00 sleep.
