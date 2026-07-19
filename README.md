# Payout Management System (LLD)

## 📌 System Overview
This is a Low-Level Design (LLD) implementation of a User Payout Management System for affiliate sales. The system handles automated advance payouts, admin reconciliations (approvals/rejections), and user withdrawals while strictly enforcing business rules and edge-case recoveries.

**Tech Stack:**
* **Backend:** FastAPI (Python)
* **Frontend:** Streamlit
* **Database:** SQLite (via SQLAlchemy ORM)

---

## 🗄️ Database Schema & Relationships

The system relies on four primary entities. 

1. **User**
   * `id` (PK)
   * `username` / `email`
   * `withdrawable_balance` (Float) - Tracks available funds.

2. **Sale**
   * `id` (PK)
   * `user_id` (FK -> User.id)
   * `brand` (String)
   * `earning` (Float)
   * `status` (String) - pending, approved, rejected
   * `advance_paid` (Boolean) - Prevents double-processing.
   * `advance_amount` (Float)

3. **Withdrawal**
   * `id` (PK)
   * `user_id` (FK -> User.id)
   * `amount` (Float)
   * `status` (String) - pending, completed, failed, cancelled, rejected
   * `created_at` (DateTime)

4. **Payout (Audit Ledger)**
   * `id` (PK)
   * `user_id` (FK -> User.id)
   * `sale_id` (FK -> Sale.id)
   * `amount` (Float)
   * `payout_type` (String) - advance, final, adjustment

**Relationships:**
* A `User` has a One-to-Many relationship with `Sale`, `Withdrawal`, and `Payout`.
* A `Sale` has a One-to-One relationship with `Payout` records to track exact financial movements per item.

---

## ⚙️ Key Design Decisions & Trade-offs

1. **The Payout Ledger (Audit Trail):**
   Instead of just blindly updating the `User.withdrawable_balance`, the system creates a `Payout` record for every financial event (advance, final payout, or negative adjustment). 
   * *Trade-off:* This consumes more database storage, but it is critical for financial systems to have a strict audit trail in case a user disputes their balance.

2. **Zero-Floor Balance for Rejected Sales:**
   If a user has a `0` balance and a previous sale is rejected, the system calculates the negative adjustment (clawing back the advance). I made the design decision to cap the user's withdrawable balance at `0` rather than letting it drop into the negatives.
   * *Trade-off:* This prevents UI confusion (users seeing negative debt), but requires the system to absorb the micro-loss until future sales offset it.

3. **Advance Payout Flagging:**
   I introduced an `advance_paid` boolean on the `Sale` table. This operates as an idempotent lock. Even if the Advance Payout CRON job / API is triggered 100 times, the database will explicitly reject processing the same sale twice.

---

## 🛡️ Edge Cases & Failure Scenarios Handled

* **Double Advance Prevention:** A sale can never receive the 10% advance twice, strictly enforced at the database query level.
* **Insufficient Funds:** Users cannot withdraw more than their current `withdrawable_balance`.
* **24-Hour Rate Limiting:** The withdrawal API checks the `created_at` timestamp of the user's last withdrawal and rejects requests made within a 24-hour window.
* **Failed Payout Recovery:** If a withdrawal fails, is rejected, or cancelled, a dedicated admin webhook endpoint refunds the exact amount back to the user's `withdrawable_balance` and locks the withdrawal status to prevent double-refunding.
* **Invalid Reconciliation State:** The system rejects attempts to reconcile a sale that is already marked as `approved` or `rejected`.
