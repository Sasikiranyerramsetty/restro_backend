# Restro Backend

A restaurant backend API built with FastAPI and MongoDB, featuring user authentication and role-based access control.

## Features

- 🔐 JWT-based authentication
- 👥 Role-based access control (Admin, Employee, Customer)
- 🍃 MongoDB database integration
- 📝 Customer signup and user login
- 🛡️ Password hashing and security
- 📚 Auto-generated API documentation
- ☁️ MongoDB Atlas cloud database

## User Roles

- **Admin**: Full system access
- **Employee**: Limited access for restaurant staff
- **Customer**: Customer access (only role that can sign up)

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed
2. **MongoDB Atlas account** (cloud database)

### Database Setup

The application is configured to use MongoDB Atlas cloud database:
- **Database**: `users_db`
- **Connection**: MongoDB Atlas cluster
- **Collections**: `users`

No local database setup required - everything runs in the cloud!

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**:
   ```bash
   python main.py
   ```
   or
   ```bash
   uvicorn main:app --reload
   ```

The MongoDB connection is automatically established when the server starts.

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Customer registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info
- `GET /api/v1/auth/profile` - Get user profile

### Users
- `POST /api/v1/users/signup` - User registration
- `POST /api/v1/users/login` - User login
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users` - Get all users
- `PATCH /api/v1/users/{user_id}/status` - Update user status

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation
- `GET /health` - Health check endpoint

## Development

The project structure:
```
restro_backend/
├── app/           # Application logic and schemas
├── db/            # MongoDB connection
├── routes/        # API routes
├── services/      # Business logic services
├── main.py        # FastAPI application
├── config.py      # Configuration settings
└── requirements.txt
```

## Security Notes

- Change the `SECRET_KEY` in `.env` for production
- Use strong passwords in production
- Enable HTTPS in production
- Regularly update dependencies
