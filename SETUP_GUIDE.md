# Quick Setup Guide

## Your MongoDB Configuration
✅ **Connected to MongoDB Atlas cluster**
- Database: `users_db`
- Connection: MongoDB Atlas (cloud)
- Collections: `users`

## Step 1: Install Python (if not installed)
1. Download Python from https://python.org
2. Make sure to check "Add Python to PATH" during installation
3. Restart your terminal/command prompt

## Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 3: Start the Server
```bash
python main.py
```

## Your Configuration
- **Database**: `users_db` (MongoDB)
- **Connection**: MongoDB Atlas cluster
- **Collections**: `users`

## API Endpoints
Once running, you can access:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: GET http://localhost:8000/health
- **User Signup**: POST http://localhost:8000/api/v1/users/signup
- **User Login**: POST http://localhost:8000/api/v1/users/login
- **Auth Signup**: POST http://localhost:8000/api/v1/auth/signup
- **Auth Login**: POST http://localhost:8000/api/v1/auth/login

## Test the API
You can test the signup endpoint with:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "password": "password123"
}
```

## MongoDB Features
- **Document-based storage**: Flexible schema for user data
- **Automatic scaling**: MongoDB Atlas handles scaling
- **High availability**: Replica set configuration
- **Secure connection**: SSL/TLS encrypted connection
