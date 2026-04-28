complaint_management/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app creation, middleware, CORS, startup
│   ├── config.py             # Settings from environment
│   ├── models/
│   │   ├── __init__.py
│   │   └── complaint.py      # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── complaint_service.py  # Business logic, JSON read/write with locking
│   ├── routes/
│   │   ├── __init__.py
│   │   └── complaint_routes.py   # API endpoints
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── error_handler.py      # Exception handling middleware
│   └── utils/
│       ├── __init__.py
│       └── logger.py             # Logging configuration
├── data/
│   └── complaints.json           # (could be created at runtime)
├── requirements.txt
├── .env.example
└── README.md