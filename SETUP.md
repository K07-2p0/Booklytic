# Booklytic Setup Guide

## Project Structure

```
Booklytic/
├── backend/          # Python FastAPI (Port 8000)
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── rotas/
└── login/            # Node.js Auth + React Frontend (Port 3000/5173)
    ├── app.js
    ├── client/       # Vite React App
    ├── controllers/
    ├── middleware/
    ├── models/
    └── routes/
```

## Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL (for Python backend)
- MongoDB (for Node.js auth)

## Running the Applications

### 1. Node.js Auth Service (Port 3000)

```bash
cd login
npm install
# Create .env file:
echo "DATABASE_URL=mongodb://localhost:27017/booklytic" > .env
echo "JWT_SECRET=your-super-secret-key-here" >> .env
echo "PORT=3000" >> .env
npm start
```

### 2. React Frontend (Port 5173)

```bash
cd login/client
npm install
npm run dev
```

### 3. Python FastAPI Backend (Port 8000)

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
# Create .env file:
echo "DATABASE_URL=postgresql://user:password@localhost:5432/booklytic_db" > .env

# Run the server
uvicorn main:app --reload
# Or:
python main.py
```

## API Documentation

Once running, Python backend docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Node.js Auth (Port 3000)
- `POST /api/v1/register` - User registration
- `POST /api/v1/login` - User login (sets httpOnly cookie)
- `POST /api/v1/logout` - User logout
- `GET /api/v1/dashboard` - Protected route

### Python FastAPI (Port 8000)
- `POST /api/v1/utilizadores` - Create user
- `GET /api/v1/utilizadores` - List users
- `POST /api/v1/login` - Authenticate user
- `POST /api/v1/marcacoes` - Create appointment
- `GET /api/v1/marcacoes` - List appointments
- `POST /api/v1/equipamentos` - Create equipment
- `GET /api/v1/equipamentos` - List equipment

## Security Improvements Made

1. Removed `.env` from git tracking
2. Increased password minimum to 8 characters
3. Implemented httpOnly cookies for JWT
4. Added proper CORS configuration
5. Fixed React dependency warnings
