# Morning Cycle — Full Operational Playbook (v2 — ACTION-FIRST)

Run at 05:00 Amsterdam time. Must complete before 05:30 so Dan's environment is clean
when he sits down for Flow Block 1 at 05:32.

**v2 CHANGE: This cycle DOES the cleanup. It doesn't write reports about what should
be cleaned. It archives, labels, moves, and deletes — then summarizes what it did.**

---

## Phase 1: SCAN + ACT — Email Cleanup

Process accounts in priority order: Gmail → iCloud → Hustle1000.

### Step 1: Gmail (deenikdaniel@gmail.com) — SCAN via API

Use `gmail_search_messages` to pull unread emails. Classify each by sender/subject
into the batch categories defined in SKILL.md.

Build a cleanup plan: which emails go in which batch, what labels to apply, what to
flag for Dan.

### Step 2: Gmail — ACT via Chrome MCP

Open Gmail in Chrome: `navigate` to `https://mail.google.com`

Execute the 6 batches defined in SKILL.md, in order:

**BATCH 1 — NEWSLETTERS:**
1. In Gmail search bar, type: `from:(seekingalpha.com OR coingecko.com OR spinach.ai OR substack.com OR sifted.eu OR datadrivenvc OR dutchfluency.com OR quiverquant.com) is:unread older_than:2d`
2. Click "Select all conversations that match this search"
3. Press `l` → type "03 Growth/Newsletters" → apply
4. Press `e` to archive all
5. Record count for brief

**BATCH 2 — RECEIPTS & TRANSACTIONAL:**
1. Search: `from:(noreply OR no-reply OR receipt OR invoice OR wiebetaaltwat OR marktplaats OR treatwell OR bunq OR stripe OR anthropic OR klarna) -in:sent is:unread`
2. Select all → Label "02 Personal/Finance & Receipts" → Archive
3. Record count

**BATCH 3 — PROMOTIONS:**
1. Search: `category:promotions older_than:1d`
2. Select all → Archive (no label needed)
3. Record count

**BATCH 4 — SECURITY ALERTS:**
1. Search: `from:(accounts.google.com OR noreply@google.com) subject:(security OR alert OR sign-in) is:unread`
2. DO NOT archive — read each one, note details in brief for Dan to verify

**BATCH 5 — CONSULTING / HUSTLE1000:**
1. Search: `to:deenikdaniel@hustle1000.com is:unread -subject:(invoice OR payment OR billing)`
2. Select all → Label "01 Work & Business/Consulting" → Archive
3. Exception: if any email involves money or active deliverable, KEEP and flag

**BATCH 6 — HUMAN EMAILS:**
1. Search: `is:unread -category:promotions -category:updates -category:social -category:forums -from:noreply -from:no-reply`
2. Read each individually. For each:
   - Needs action → Label "04 Action Required/Awaiting Reply", keep in inbox
   - Info only → appropriate label → Archive
   - Payment/money → ALWAYS flag in brief
3. For high-priority items requiring a reply, use `gmail_create_draft` to prepare a response

### Step 3: iCloud (deenikdaniel@icloud.com)

If iCloud email MCP or Apple Mail via computer-use is available:
- Same triage logic but lighter — personal only
- Focus on: Apple purchases, iCloud storage, personal contacts
- Health-related → flag (72kg goal)
- Travel/Mallorca → flag (relocation goal)

If no access: note in brief. Suggest connecting.

### Step 4: Hustle1000 (deenikdaniel@hustle1000.com)

If accessible (separate Gmail login in Chrome or MCP):
- Only scan for active client emails + money
- Everything else: archive silently
- If client email found: flag with "Consulting — handle quickly to accelerate exit"

If no access: note in brief.

### Step 5: Record Cleanup Metrics

After all batches:
- Total emails archived (by batch)
- Total emails labeled
- Drafts created
- Items flagged for Dan
- Remaining unread count

---

## Phase 2: SWEEP — Directory Cleanup

### If computer-use is available:

1. `request_access` for Finder
2. `screenshot` current Desktop
3. `screenshot` current ~/Downloads (open in Finder)
4. For each visible file, apply the routing rules from SKILL.md:
   - PDFs → Documents/Finance/2026/ or Documents/Legal/
   - Images → Documents/Photos/YYYY-MM/
   - Installers (.dmg/.pkg) older than 7 days → Trash
   - Code files → workspace or project directory
   - Everything else older than 30 days → Trash
5. Move files using Finder drag-and-drop or right-click → Move to
6. Verify Desktop is EMPTY with a final screenshot
7. Check Trash size — if over 1GB, empty it

### If computer-use is NOT available (scheduled task):

Generate a specific, actionable file-routing checklist:
```
FILES TO MOVE (execute in < 2 min):
□ ~/Downloads/invoice-anthropic-apr.pdf → ~/Documents/Finance/2026/2026-04-09_anthropic_receipt.pdf
□ ~/Downloads/photo-2026-04-08.jpg → ~/Documents/Photos/2026-04/
□ ~/Desktop/notes.txt → [Workspace]/Journals/2026-04/2026-04-08_notes.md
□ ~/Downloads/SomeApp.dmg → Trash (installed 2 weeks ago)
```

Keep it under 10 items. Batch similar files.

---

## Phase 3: ORGANIZE — Journal + Calendar

### Journal Organization

1. Check Apple Notes (via MCP) for entries from yesterday
2. Scan workspace and Downloads for .md/.txt journal-like files
3. Move/copy to `Journals/YYYY-MM/` with standardized names
4. Never delete originals

### Calendar Hygiene

1. `gcal_list_events` for today's date
2. Flag double-bookings or conflicts
3. Identify flow block opportunities:
   - 05:32-08:30 = Flow Block 1 (protected)
   - 10:00-13:00 = Flow Block 2 target
   - 14:30-17:30 = Flow Block 3 target
4. Note any prep needed for meetings

---

## Phase 4: BRIEF — Generate Morning Summary

Compile into the Morning Brief format from SKILL.md.

**Key change from v1:** The brief now leads with ACTIONS TAKEN, not "things that need
to be cleaned." By the time Dan reads this, the cleaning is already done.

**Delivery:** Apple Notes > Notion > workspace markdown file (`Reports/morning-brief-YYYY-MM-DD.md`)

**Day number:** Day 1 = January 1, 2026. Calculate from today's date.

**Identity affirmation:** Based on day-of-week rotation.

**Keep it under 2 minutes reading time.** Dan scans this before his first flow block.
