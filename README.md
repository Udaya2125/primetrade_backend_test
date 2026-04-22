# PrimeTrade Tasks Management App

A production-grade task management application built with FastAPI, MongoDB Atlas, and React. Features microservice architecture with load balancing, OAuth2 authentication, and a full-featured React UI.

## 📋 Project Overview

**Backend**: FastAPI (Python 3.13) microservices with JWT authentication
**Frontend**: React 18 + Vite with Axios and React Router
**Database**: MongoDB Atlas (cloud-hosted)
**Orchestration**: Docker Compose with Nginx load balancing
**Architecture**: Microservices (Auth + Tasks services) with 2 replicas each behind a gateway

## ✨ Features

- ✅ User registration and authentication (OAuth2 form-based)
- ✅ JWT token-based session management (60-minute expiry)
- ✅ Task creation, reading, updating, and deletion (CRUD)
- ✅ Task status toggle (complete/incomplete)
- ✅ Protected routes (authenticated users only)
- ✅ Load balancing and horizontal scaling (2 replicas per service)
- ✅ Async MongoDB integration with Motor
- ✅ Comprehensive API documentation (Swagger UI)

---

## 🚀 Quick Start (For Evaluators)

### Prerequisites

Ensure you have installed:
- **Docker** (v24+) and **Docker Compose** (v2.20+)
- **Node.js** (v18+) and **npm**
- **Python** (v3.13+) - for local development only

### Step 1: Clone and Setup

```bash
cd c:\Users\udaya\Documents\primetrade
# No additional setup needed - all configs are in place
```

### Step 2: Start All Services (Docker Compose)

```bash
docker compose up -d
```

This starts 6 containers:
- `mongo` - MongoDB local database (optional, Atlas is primary)
- `auth1` & `auth2` - Auth service replicas
- `tasks1` & `tasks2` - Tasks service replicas
- `nginx-gateway` - Load balancer and reverse proxy

**Verify services are running:**
```bash
docker compose ps
```

### Step 3: Access the Application

1. **Frontend (React UI)**: http://localhost:5173
2. **Nginx Gateway**: http://localhost:8080
3. **Auth Service Docs**: http://localhost:8080/auth/docs
4. **Tasks Service Docs**: http://localhost:8080/tasks/docs

---

## 📝 Testing Checklist for Evaluators

### Phase 1: Service Health Check ✅

1. **Verify all containers are running:**
   ```bash
   docker compose ps
   ```
   Expected: All 6 containers in `Up` state

2. **Check gateway routes:**
   - Auth docs: `curl http://localhost:8080/auth/docs` → HTTP 200
   - Tasks docs: `curl http://localhost:8080/tasks/docs` → HTTP 200
   - Health: `curl http://localhost:8080/` → HTTP 200

### Phase 2: Frontend Authentication Flow 🔐

1. **Open frontend**: http://localhost:5173
2. **Register a new user:**
   - Click "Register" button
   - Fill in: Full Name, Email, Password
   - Example: `testuser@example.com` / `password123`
   - Click "Register" → Should redirect to Login page
3. **Login:**
   - Enter the email and password from registration
   - Click "Login" → Should redirect to Dashboard
4. **Verify authentication:**
   - Token should be stored in browser localStorage (`access_token`)
   - Navbar should show "Logout" button (user is authenticated)

### Phase 3: Task CRUD Operations 📋

Once logged in on Dashboard:

1. **Create a Task:**
   - In "Create Task" form, enter:
     - Title: "Complete project documentation"
     - Description: "Write comprehensive README for evaluators"
   - Click "Create Task"
   - Expected: Task appears in list below with status "Incomplete"

2. **View Tasks:**
   - All tasks should display with:
     - Title
     - Description
     - Status badge (Incomplete/Complete)
     - Action buttons (Toggle Complete / Delete)

3. **Toggle Task Status:**
   - Click "Toggle Complete" on a task
   - Expected: Status changes from "Incomplete" → "Complete" (or vice versa)
   - Click again to revert

4. **Delete a Task:**
   - Click "Delete" button on a task
   - Expected: Task is immediately removed from the list
   - Backend confirms deletion

### Phase 4: Load Balancing Verification ⚖️

1. **Check service replicas:**
   ```bash
   docker compose logs auth1 | tail -20
   docker compose logs auth2 | tail -20
   docker compose logs tasks1 | tail -20
   docker compose logs tasks2 | tail -20
   ```

2. **Observe load distribution:**
   - Each login/task operation routes through Nginx to whichever replica is available
   - No single point of failure

### Phase 5: API Documentation 📚

1. **Auth Service Swagger UI**: http://localhost:8080/auth/docs
   - Available endpoints:
     - `POST /auth/login` - User login (returns JWT token)
     - `POST /auth/register` - User registration
     - `GET /users/me` - Get current user profile

2. **Tasks Service Swagger UI**: http://localhost:8080/tasks/docs
   - Available endpoints:
     - `GET /tasks/` - List all tasks for logged-in user
     - `POST /tasks/` - Create a new task
     - `PATCH /tasks/{task_id}` - Update task (toggle status)
     - `DELETE /tasks/{task_id}` - Delete a task

---

## 📂 Project Structure

```
primetrade/
├── backend/
│   ├── app/
│   │   ├── core/              # JWT, password hashing, settings
│   │   ├── db/                # MongoDB Motor connection
│   │   ├── controllers/       # Business logic (auth, users, tasks)
│   │   ├── routes/            # API endpoints
│   │   ├── main_auth.py       # Auth microservice entry point
│   │   └── main_tasks.py      # Tasks microservice entry point
│   ├── Dockerfile             # Container image definition
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Database credentials (Atlas URI)
│
├── frontend/
│   ├── src/
│   │   ├── pages/             # Login, Register, Dashboard pages
│   │   ├── components/        # Navbar, UI components
│   │   ├── services/          # API client, auth token management
│   │   ├── App.jsx            # Main routing + route protection
│   │   └── styles.css         # Global styling
│   ├── package.json           # Node.js dependencies
│   └── vite.config.js         # Vite build configuration
│
├── nginx/
│   └── nginx.conf             # Load balancer config, route rules
│
├── docker-compose.yml         # Multi-container orchestration
└── README.md                  # This file
```

---

## 🔧 Configuration Details

### Database
- **Primary**: MongoDB Atlas (cloud)
- **Connection**: Configured via `MONGODB_URI` environment variable in `.env`
- **Database**: `tasks_app`
- **Collections**: `users`, `tasks`

### API Gateway (Nginx)
- **Port**: 8080
- **Routes**:
  - `/api/v1/auth/*` → Auth service (load balanced: auth1:8000, auth2:8000)
  - `/api/v1/users/*` → Auth service (load balanced)
  - `/api/v1/tasks/*` → Tasks service (load balanced: tasks1:8000, tasks2:8000)

### Authentication
- **Scheme**: OAuth2PasswordBearer (username/password form-based)
- **Token Format**: JWT (HS256 algorithm)
- **Token Expiry**: 60 minutes
- **Storage**: Browser localStorage (`access_token` key)

---

## 🛠️ Local Development (Alternative to Docker)

### Start Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Auth service available at: http://localhost:8000/docs

### Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: http://localhost:5173

**Note**: In dev mode, frontend makes requests directly to `http://localhost:8000` (not through Nginx gateway)

---

## 📊 Microservices Architecture

```
┌─────────────────┐
│   React UI      │
│ (localhost:5173)│
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  Nginx Gateway      │
│ (localhost:8080)    │
└────┬────────────┬───┘
     │            │
     ▼            ▼
 ┌──────┐    ┌─────────┐
 │Auth  │    │  Tasks  │
 │   1  │    │    1    │
 │:8000 │    │  :8000  │
 └──────┘    └─────────┘
     ▲            ▲
     │            │
 ┌──────┐    ┌─────────┐
 │Auth  │    │  Tasks  │
 │   2  │    │    2    │
 │:8000 │    │  :8000  │
 └──────┘    └─────────┘
     │            │
     └──────┬─────┘
            ▼
      ┌─────────────────┐
      │ MongoDB Atlas   │
      │   (Cloud DB)    │
      └─────────────────┘
```

---

## 🧪 Testing Endpoints (cURL Examples)

### Register User
```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "full_name": "Test User",
    "password": "password123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser@example.com&password=password123"
```

Response: `{"access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...", "token_type": "bearer"}`

### Create Task (with token)
```bash
curl -X POST http://localhost:8080/api/v1/tasks/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample task",
    "description": "This is a test task"
  }'
```

### Get All Tasks
```bash
curl -X GET http://localhost:8080/api/v1/tasks/ \
  -H "Authorization: Bearer {access_token}"
```

---

## 🐛 Troubleshooting

### Issue: Containers won't start
**Solution:**
```bash
docker compose down
docker compose up --build
```

### Issue: Port 8080 already in use
**Solution:**
```bash
# Find process using port 8080
netstat -ano | findstr :8080
# Kill process or change port in docker-compose.yml
```

### Issue: Frontend can't connect to API
**Solution:**
1. Verify gateway is running: `docker compose ps | grep nginx`
2. Check API is accessible: `curl http://localhost:8080/api/v1/auth/`
3. Verify token in localStorage: Browser DevTools → Application → localStorage → `access_token`

### Issue: MongoDB connection error
**Solution:**
1. Verify Atlas URI in `backend/.env` is correct
2. Check network access rules in MongoDB Atlas: Allow IP 0.0.0.0/0 (or your IP)
3. Verify credentials: username and password are correct

---

## 📞 Support

For issues or questions, check:
1. Backend logs: `docker compose logs auth1 auth2 tasks1 tasks2`
2. Gateway logs: `docker compose logs nginx-gateway`
3. Browser console: Check for frontend errors (DevTools → Console)

---

**Last Updated**: April 2026
**Version**: 1.0.0 Production