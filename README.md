# Payout Management System

## 📌 System Overview
This is a Low-Level Design (LLD) implementation of a User Payout Management System for affiliate sales. The system handles automated advance payouts, admin reconciliations (approvals/rejections), and user withdrawals while strictly enforcing business rules and edge-case recoveries.

## 📁 Project Structure

```text
payout-management/
│
├── app/
│   ├── routes/
│   │   ├── users.py
│   │   ├── sales.py
│   │   ├── payouts.py
│   │   └── withdrawals.py
│   │
│   ├── services/
│   │   ├── payout_service.py
│   │   ├── withdrawal_service.py
│   │   └── reconciliation_service.py
│   │
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── main.py
│   └── frontend.py
│
├── requirements.txt
├── README.md
└── .gitignore

---

```markdown

```

---

## ✨ Features

### User Management

* Create Users
* View Users

### Sales Management

* Create Sales
* View Sales
* Track pending sales

### Advance Payout

* Calculates 10% advance payout for every eligible pending sale.
* Prevents duplicate advance payouts for the same sale using an idempotent database lock.

### Reconciliation

Admin can reconcile sales by marking them as:

* **Approved:** The system automatically calculates the remaining payout after deducting the advance already paid.
* **Rejected:** The system adjusts the user's balance to claw back the advance paid.

### Withdrawal

* Users can withdraw available balance.
* Restricts withdrawals to one every 24 hours.

### Failed Payout Recovery

If a withdrawal fails or gets cancelled:

* Credits the amount back to the user's withdrawable balance.
* Updates the status to prevent duplicate refunds.

---

## 🗄️ Database Design

### Users

| Column | Type | Description |
| --- | --- | --- |
| id | Integer (PK) | Unique identifier |
| username | String | User's handle |
| email | String | User's email |
| withdrawable_balance | Float | Tracks available funds |

### Sales

| Column | Type | Description |
| --- | --- | --- |
| id | Integer (PK) | Unique identifier |
| user_id | Integer (FK) | Reference to User |
| brand | String | The brand of the sale |
| earning | Float | Total value of the sale |
| status | String | pending, approved, rejected |
| advance_paid | Boolean | Lock to prevent duplicate advances |
| advance_amount | Float | The 10% advance amount given |

### Payouts (Audit Ledger)

| Column | Type | Description |
| --- | --- | --- |
| id | Integer (PK) | Unique identifier |
| user_id | Integer (FK) | Reference to User |
| sale_id | Integer (FK) | Reference to Sale |
| amount | Float | Amount transacted |
| payout_type | String | advance, final, adjustment |
| status | String | completed |

### Withdrawals

| Column | Type | Description |
| --- | --- | --- |
| id | Integer (PK) | Unique identifier |
| user_id | Integer (FK) | Reference to User |
| amount | Float | Amount requested |
| status | String | pending, completed, failed, cancelled, rejected |
| created_at | DateTime | Used to enforce the 24-hour rule |

---

## 🌐 API Endpoints

### Users

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/users/` | Create a new user |
| GET | `/users/` | Get all users |
| GET | `/users/{id}` | Get specific user |

### Sales & Reconciliation

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/sales/` | Create a new sale (defaults to pending) |
| GET | `/sales/` | Get all sales |
| PUT | `/sales/{sale_id}/reconcile` | Reconcile a sale (approved/rejected) |

### Advances

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/advances/process/{user_id}` | Batch-process 10% advance for all pending sales |

### Withdrawals & Recovery

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/withdrawals/` | Request a withdrawal (24hr limit enforced) |
| PUT | `/withdrawals/{withdrawal_id}/status` | Handle failed/cancelled withdrawals and refund balance |

---

## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone [https://github.com/](https://github.com/)<your-username>/payout-management.git
cd payout-management

```

### 2. Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate

```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Run Backend

```bash
uvicorn app.main:app --reload

```

* Backend runs on: `http://127.0.0.1:8000`
* Swagger UI: `http://127.0.0.1:8000/docs`

### 5. Run Frontend

Open a second terminal and run:

```bash
streamlit run app/frontend.py

```

* Frontend runs on: `http://localhost:8501`

---

## ⚙️ Design Decisions & Trade-offs

* **The Payout Ledger (Audit Trail):** Instead of just blindly updating the `withdrawable_balance`, the system creates a `Payout` record for every financial event (advance, final payout, or negative adjustment). *Trade-off:* This consumes more database storage, but it is critical for financial systems to have a strict audit trail in case a user disputes their balance.
* **Zero-Floor Balance for Rejected Sales:** If a user has a `0` balance and a previous sale is rejected, the system calculates the negative adjustment. The system caps the user's withdrawable balance at `0` rather than letting it drop into the negatives. *Trade-off:* This prevents UI confusion (users seeing negative debt), but requires the system to absorb the micro-loss until future sales offset it.
* **FastAPI + Streamlit:** FastAPI was selected for its high performance and automatic Swagger API documentation. Streamlit provides a rapid, component-based frontend for interacting with the APIs without requiring a separate JavaScript framework.
* **Service Layer Pattern:** Business logic (math, reconciliation, validations) is separated into `services/` modules to improve maintainability and keep API routers lightweight.

---

## 📸 Screenshots

*<img width="1867" height="823" alt="ss1" src="https://github.com/user-attachments/assets/67340495-cf93-43bc-90aa-ad895ebf32f4" /><img width="1907" height="827" alt="ss2" src="https://github.com/user-attachments/assets/c563174d-add8-4c45-953c-3fbe747f7e50" />

*

---

## 🧑‍💻 Author

**Anupriya**

GitHub: https://github.com/camren88


```

```
