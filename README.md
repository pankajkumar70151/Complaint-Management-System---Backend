# Complaint Management System - Backend

A production‑ready REST API for managing complaints, built with **FastAPI** and **Python**, using a **JSON file** for persistence (no database required).

**Features:**
- Full CRUD operations for complaints (create, read, update status, delete)
- Pagination, filtering by status, keyword search, and sorting (by date)
- Automatic Swagger/OpenAPI documentation
- Thread‑safe JSON file storage
- Modular architecture (routes, services, models, middleware)
- Production extras: logging, CORS, exception handling middleware, environment‑based configuration

---

## Project Structure
complaint_management/
├── app/
│ ├── init.py
│ ├── main.py # FastAPI app setup, middleware, CORS
│ ├── config.py # Environment settings (Pydantic Settings)
│ ├── models/
│ │ ├── init.py
│ │ └── complaint.py # Pydantic models (request/response)
│ ├── services/
│ │ ├── init.py
│ │ └── complaint_service.py # Business logic & thread‑safe file store
│ ├── routes/
│ │ ├── init.py
│ │ └── complaint_routes.py # API endpoints (router)
│ ├── middleware/
│ │ ├── init.py
│ │ └── error_handler.py # Global exception handler
│ └── utils/
│ ├── init.py
│ └── logger.py # Logging configuration
├── data/ # Persistent JSON storage (auto‑created)
├── requirements.txt
├── .env.example # Example environment variables
└── README.md



---

## Technology Stack

- **Python 3.9+**
- **FastAPI** – web framework
- **Pydantic** – data validation & settings management
- **Uvicorn** – ASGI server
- **JSON** – file‑based storage (no SQL/NoSQL database)

---

## Setup and Installation

### 1. Clone or copy the project

```bash
git clone <your-repo-url> complaint_management
cd complaint_management


python -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

pip install -r requirements.txt

#Run app

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload