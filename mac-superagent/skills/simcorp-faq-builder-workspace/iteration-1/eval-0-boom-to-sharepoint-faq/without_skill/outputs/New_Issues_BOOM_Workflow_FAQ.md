# New Issues Workflow (incl. BOOM / Money-Market) — FAQ

**Audience:** Portfolio Managers and Traders booking primary-market new issues in SimCorp Dimension.
**Scope:** How to create a shell for a new issue in Asset Manager, route it to Order Manager, match it against Bloomberg, and how to test money-market programmes in Bloomberg BOOM (UAT/BETA).
**Grounding:** Steps are grounded in the SimCorp manual *Simulations in Asset Manager* (September 2025) — hereafter **[Sim-AM]**. BOOM steps are Bloomberg-terminal actions (vendor side); the only SimCorp touchpoint there is the inbound FIX drop copy.

> How to read this page: the workflow has **three phases**. Each step lists the action, the screenshot that shows it, and (where applicable) a **Manual grounding** note confirming the behaviour against [Sim-AM]. See `workflow_diagram.svg` for the annotated end-to-end picture.

---

## At a glance

| Phase | Where | Goal | Screenshots |
|---|---|---|---|
| 1. Create a shell for the new issue | Asset Manager → Create Simulations | Stand up a preliminary "shell" security and a simulation for the new issue | step1-1, step1-2, step1-3 |
| 2. Route to Order Manager & match | Order Manager → Match Unsolicited Execution | Accept the trade, pull the real security from Bloomberg, validate against compliance, allocate | step2-1, step2-2 |
| 3. Access to BOOM in UAT | Bloomberg terminal (BOOM / FAXT BETA) | Test money-market programmes and place a test trade that FIX-drops back to SimCorp | step3-1, step3-2, step3-3 |

---

## Phase 1 — Create a shell for the new issue (Asset Manager)

A new issue often does not yet exist as a full security in SimCorp Dimension (no final ISIN/CUSIP). You therefore create a lightweight **preliminary "shell"** by cloning an existing, similar bond, so you can raise the order now and enrich the true security later.

### Q1. How do I start a shell for a new issue?
1. Open a new **Create Simulations** tab (Simulations applet → **New**).
2. Right-click a column header → **Select Fields** and add the **"New Issue –"** columns to the grid (e.g. *New Issue – Existing Security ID, New Issue – ISIN, New Issue – Coupon rate, New Issue – Coupon term length, New Issue – Maturity date, New Issue – Security ID, New Issue – Quotation*).

![Add the New Issue columns to the Create Simulations grid](screenshots/step1-1_new-issue-columns.png)
*Screenshot step1-1 — the "New Issue –" columns highlighted in the Create Simulations grid. Note the `PRIMARY_MKT` value that appears for a primary-market new issue.*

> **Manual grounding [Sim-AM §2.1.2 / §2.1.3]:** New-issue fields are created directly in the Create Simulations window (instead of the Bonds – Preliminary Data window). They carry the prefix **"New Issue –"** and must be added via **Select Fields**. When you base a new issue on an existing bond, the New Issue – ISIN field is defaulted to **`PRIMARY_MARKET`** until the real published ISIN is available.

### Q2. Which security should I clone?
Choose an existing security that is **similar in nature** to the new issue (same currency, coupon structure, etc.) and enter its ISIN in the **"New Issue – Existing Security ID"** field.

> **Manual grounding [Sim-AM §2.1.3]:** Supported proxies are bullet bonds, zero-coupon bonds, floating bullet bonds and US pool. Cloning copies the proxy's interest/redemption and market conventions (quote type, factor), free codes, classification schemes, ratings and security group codes onto the new-issue simulation. All copied values can be overridden.

### Q3. What do I fill in to define the shell?
Complete the fields that make the shell specific:
- **Maturity Date** (a tenor such as `5Y` is calculated off the issue date)
- **Coupon Rate**
- A name in the **"New Issue – Security ID"** field (the mandatory Security ID / Security No.)

Then click **Save New Issue** to create the shell.

![Save New Issue creates the preliminary shell](screenshots/step1-2_save-new-issue-shell.png)
*Screenshot step1-2 — the completed New Issue row with the **Save New Issue** button highlighted (alongside Create All / Clear All / Cancel).*

> **Manual grounding [Sim-AM §2.1.2 / §2.1.3, step 10]:** **Save New Issue** creates the new-issue security as a simulation in the Simulations applet, saved as a **preliminary bond** (the *Preliminary* flag is set). A new issue is **not** created if it duplicates an existing security — a warning is shown.

### Q4. What happens after I save, and what must I tick before releasing?
After you click **Save New Issue**, the New Issue input fields clear and you can build your simulation normally. Before you release the trade to Order Manager, make sure the **"Primary market"** box is **ticked** on the simulation row.

![Tick Primary market before releasing to Order Manager](screenshots/step1-3_primary-market-tick.png)
*Screenshot step1-3 — the **Primary market** checkbox ticked on the simulation in the Simulations (1) tab.*

> **Manual grounding [Sim-AM]:** On **Create and Release**, Order Manager automatically launches a **pre-trade compliance validation** and only releases the order if it passes. (The primary-market flag marks the order as a primary-market issuance so it follows the new-issue / shell path rather than the secondary-market path.)

---

## Phase 2 — Route to Order Manager and match against Bloomberg

Once released, the order lands in Order Manager as an unsolicited execution to be matched against the real security data from Bloomberg. This is where the shell is replaced by the true new-issue security.

### Q5. How do I accept the released trade?
In **Order Manager**, right-click the trade you just released from Asset Manager and select **Accept**. Then right-click the **VCON** and select **Match**.

### Q6. How do I pull the real security details from Bloomberg?
In the **Match Unsolicited Execution** window, under **Security Selection**, choose an identifier from the dropdown (e.g. **CUSIP**), enter the identifier, and click **Request** to pull the security details from Bloomberg.

![Request pulls the security from Bloomberg in the Match window](screenshots/step2-1_vcon-match-request-bloomberg.png)
*Screenshot step2-1 — the Match Unsolicited Execution window; **Security Selection** (identifier dropdown + value) and the **Request** button highlighted.*

> **Manual grounding [Sim-AM §2.1.3 "New issue flow after releasing to Order Manager"]:** After converting the simulation to an order and releasing it, you search for the security in SimCorp Dimension via the **Capture Trade** or **Match Unsolicited Executions** windows. If the security exists, you match the execution to it; if it does not, you **issue a missing-security request to the data provider** during matching. The order **shell security is then updated with the requested identifier**, and once the security is imported the **Preliminary flag is removed**, so future orders can trade it in the secondary market.

### Q7. How do I check compliance on the true security?
Once the security details are returned from Bloomberg, click **Validate**. This validates the true security's parameters against the compliance rules — necessary because the original shell was only pre-validated on proxy data, not on the real new-issue data.

![Validate runs compliance on the true security](screenshots/step2-2_validate-compliance.png)
*Screenshot step2-2 — the Match window after the Bloomberg pull; the **Validate** button highlighted (with **Match and Allocate** becoming available).*

> **Manual grounding [Sim-AM]:** Simulations/orders are subject to **pre-trade compliance validation**; because the shell was checked on proxy data, re-validating here ensures the actual new-issue security is checked against the compliance rules before allocation.

### Q8. How do I finish?
Click **Match and Allocate** to complete the match and allocate the trade to the portfolio(s).

### Notes & gotchas (from the source doc)
- **No ISIN yet?** If Bloomberg has not generated an ISIN/CUSIP for the new issue, you **cannot** match/allocate. Wait until the ISIN/CUSIP is in Bloomberg.
- **Workaround:** You can always manually **Capture** a trade and fill in the ticket based on the VCON.

---

## Phase 3 — Access to BOOM in UAT (money-market programmes, BETA)

Use Bloomberg **BOOM** in DEMO/BETA to view money-market programmes and place a **test trade** that flows back to SimCorp via FIX drop copy. *These are Bloomberg-terminal actions; the SimCorp side is the inbound FIX drop copy landing as an unsolicited execution (Phase 2).*

### Q9. How do I get into BOOM (BETA/DEMO)?
1. Run **`FAXT BETA <GO>`** on the Bloomberg terminal.
2. Run **`BOOM <GO>`** and under **99) Settings** flag **DEMO mode ON**.
3. You will then see the programmes and the Dealer **BBLP** (the test Bloomberg dealer/issuer).

![BOOM money-market programmes in DEMO mode](screenshots/step3-1_boom-programmes.png)
*Screenshot step3-1 — BOOM programme list (e.g. 7-Eleven Inc maturities) with rates in the yellow (clickable) fields.*

### Q10. How do I place a test trade?
1. Click into any **rate (yellow field)** — e.g. 7-Eleven maturing 11/21/25.
2. The **trade ticket** opens; hit **Submit** (you can switch between maturities bottom-left).
3. Once submitted, the order is **auto-accepted** and appears in your blotter.

![BOOM trade ticket — Submit to BTBU](screenshots/step3-2_boom-trade-ticket.png)
*Screenshot step3-2 — the BOOM trade ticket (Side, Quantity, Discount, Maturity, Scales) with **Submit to BTBU**. Header shows BLOOMBERG D1 DEMO.*

### Q11. How do I confirm it and see what flows to SimCorp?
Run **`BLOT <GO>`** to see the ticket in your blotter and click into it for the trade details. After submission, the **FIX drop copy flows to SimCorp** (arriving as an unsolicited execution — handle it via Phase 2).

![BLOT blotter — trade detail that flows to SimCorp](screenshots/step3-3_blot-blotter.png)
*Screenshot step3-3 — the BLOT blotter CP window showing the accepted test CP trade (Status: Accepted, DTC Cusip, Proceeds, Ratings) that flows to SimCorp.*

> **Test it:** Try a test trade in DEMO mode and report any issues or questions.

---

## Screenshot ↔ step map

| # | File | Phase / Step | Shows |
|---|---|---|---|
| 1 | step1-1_new-issue-columns.png | P1 / Q1 | "New Issue –" columns added to Create Simulations grid (PRIMARY_MKT) |
| 2 | step1-2_save-new-issue-shell.png | P1 / Q3 | Save New Issue button on completed shell row |
| 3 | step1-3_primary-market-tick.png | P1 / Q4 | Primary market checkbox ticked on the simulation |
| 4 | step2-1_vcon-match-request-bloomberg.png | P2 / Q6 | Match window — Security Selection + Request (Bloomberg pull) |
| 5 | step2-2_validate-compliance.png | P2 / Q7 | Match window — Validate (compliance) / Match and Allocate |
| 6 | step3-1_boom-programmes.png | P3 / Q9 | BOOM programme list (DEMO) |
| 7 | step3-2_boom-trade-ticket.png | P3 / Q10 | BOOM trade ticket — Submit to BTBU |
| 8 | step3-3_blot-blotter.png | P3 / Q11 | BLOT blotter — accepted CP trade detail |

## Manual grounding summary

| Behaviour | Source |
|---|---|
| "New Issue –" fields added via Select Fields in Create Simulations; prefix logic mirrors Bonds – Preliminary Data | [Sim-AM] §2.1.2 (p.15) |
| Cloning an existing bond-like security; copied conventions/free codes/ratings; New Issue – ISIN defaults to `PRIMARY_MARKET` | [Sim-AM] §2.1.3 (p.18–19) |
| **Save New Issue** creates a preliminary bond simulation (Preliminary flag); duplicate warning | [Sim-AM] §2.1.3 step 10 (p.19) |
| New-issue flow after release: Match Unsolicited Executions / Capture Trade; missing-security request; shell updated then Preliminary flag removed | [Sim-AM] §2.1.3 "New issue flow after releasing to Order Manager" (p.19–20) |
| Pre-trade compliance validation on Create and Release | [Sim-AM] release/compliance sections |
| Update security IDs on primary-market positions (adding the published market identifier later) | [Sim-AM] §2.1.3.1 (p.21) |
| BOOM programme view, DEMO mode, trade ticket, BLOT, FIX drop copy | Bloomberg terminal (vendor side) — source workflow doc; not a SimCorp manual |

*Note: The **Match Unsolicited Execution** window's field-level Help lives in the Order Manager Getting Started manual (not held in this manual set); the new-issue behaviour of that window is nonetheless documented in [Sim-AM] as cited above.*
