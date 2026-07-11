# Banking Web Application

A full-stack banking application built with **Python Flask**, **SQLite**, and **Bootstrap**.

## Features

| Feature | Description |
|---------|------------|
| Customer Login | Secure login with hashed passwords |
| Dashboard | View current balance at a glance |
| Deposit Funds | Add money to your account |
| Withdraw Funds | Withdraw with balance validation |
| Logout | Secure session termination |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5 + Bootstrap 5 |
| Backend | Python Flask |
| Database | SQLite (file-based, embedded) |

## Project Structure

```
├── BACKEND/
│   ├── app.py                  # Flask application entry point
│   ├── database.py             # DB connection, schema, seed data
│   ├── requirements.txt        # Python dependencies
│   ├── routes/
│   │   ├── auth_routes.py      # Login / logout / status endpoints
│   │   └── account_routes.py  # Balance / deposit / withdraw endpoints
│   └── services/
│       ├── auth_service.py     # Authentication logic
│       └── account_service.py # Business logic for transactions
├── FRONTEND/
│   ├── login.html              # Login page
│   └── dashboard.html         # Dashboard with deposit & withdraw
├── tests/
│   └── test_banking.py        # Pytest unit + integration tests
└── requirements.txt
```

## Quick Start

### 1. Install dependencies

```bash
cd BACKEND
pip install -r requirements.txt
```

### 2. Run the Flask server

```bash
python app.py
```

The API starts on `http://127.0.0.1:5000`.

### 3. Open the frontend

Open `FRONTEND/login.html` in your browser.

**Demo credentials:**

| Username | Password |
|----------|----------|
| alice | alice123 |
| bob | bob123 |
| carol | carol123 |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login with username & password |
| POST | `/api/auth/logout` | Logout current session |
| GET | `/api/auth/status` | Check login status |
| GET | `/api/account/balance` | Get current balance |
| POST | `/api/account/deposit` | Deposit funds |
| POST | `/api/account/withdraw` | Withdraw funds |

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```
