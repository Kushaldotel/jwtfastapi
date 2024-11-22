# FastAPI Auth Server

## Setup Instructions

1. Clone the repository.
2. Install dependencies:


3. Set up PostgreSQL and update `DATABASE_URL` in `database.py`.
4. Run the server:


## API Endpoints
- POST `/api/v1/register-user`: Register a new user.
- POST `/api/v1/auth/login`: Login and get tokens.
- GET `/api/v1/me`: Get user profile.
- POST `/api/v1/auth/refresh-token`: Reterive refresh and access token.
