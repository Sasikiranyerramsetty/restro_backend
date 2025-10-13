# MongoDB Users API Guide

This guide explains the simple user authentication structure using MongoDB without password hashing.

## Project Structure

```
restro_backend/
├── services/
│   ├── __init__.py
│   └── users_services.py          # MongoDB operations for users
├── routes/
│   ├── __init__.py
│   └── users.py                   # User endpoints
├── db/
│   └── mongodb.py                 # MongoDB connection and utilities
└── app/
    └── schemas.py                 # Pydantic schemas for MongoDB
```

## Database Configuration

- **MongoDB Connection**: `mongodb+srv://Jagadish:Ammananna@cluster0.6evyrdj.mongodb.net/`
- **Database Name**: `users_db`
- **Collection Name**: `users`

## API Endpoints

### 1. User Signup
- **URL**: `POST /api/v1/users/signup`
- **Description**: Create a new user account in MongoDB
- **Request Body**:
```json
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "+1234567890",
    "password": "simplepassword123"
}
```
- **Response** (201 Created):
```json
{
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "+1234567890",
    "role_id": 1,
    "shift": null,
    "salary": null,
    "status": "active",
    "address": null,
    "created_at": "2024-01-01T12:00:00.000Z",
    "updated_at": null
}
```

### 2. User Login
- **URL**: `POST /api/v1/users/login`
- **Description**: Authenticate user with email and password
- **Request Body**:
```json
{
    "email": "john.doe@example.com",
    "password": "simplepassword123"
}
```
- **Response** (200 OK): User object (same as signup response)

### 3. Get User by ID
- **URL**: `GET /api/v1/users/users/{user_id}`
- **Description**: Get user information by MongoDB ObjectId
- **Response** (200 OK): User object

### 4. Get All Users
- **URL**: `GET /api/v1/users/users`
- **Description**: Get all users with pagination
- **Query Parameters**:
  - `skip` (optional): Number of records to skip (default: 0)
  - `limit` (optional): Maximum number of records (default: 100)
- **Response** (200 OK): Array of user objects

### 5. Update User Status
- **URL**: `PATCH /api/v1/users/users/{user_id}/status`
- **Description**: Update user status
- **Query Parameters**:
  - `status`: New status value
- **Response** (200 OK): Success message

## Key Features

1. **MongoDB Integration**: Uses Motor (async MongoDB driver) for database operations
2. **No Password Hashing**: Passwords are stored as plain text as requested
3. **Async Operations**: All database operations are fully async
4. **Service Layer**: Database logic is separated into `services/users_services.py`
5. **Error Handling**: Comprehensive error handling with proper HTTP status codes
6. **Validation**: Input validation using Pydantic schemas with MongoDB ObjectId support
7. **Logging**: Detailed logging for debugging

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Testing

Run the test script to verify the endpoints:

```bash
python test_users_signup.py
```

Make sure your FastAPI server is running on `http://localhost:8000` before testing.

## MongoDB Document Structure

Users are stored in the `users` collection with the following structure:

```json
{
    "_id": "ObjectId",
    "name": "string",
    "email": "string (unique)",
    "phone_number": "string (unique)",
    "password": "string (plain text)",
    "role_id": "number (default: 1)",
    "status": "string (default: 'active')",
    "shift": "string (optional)",
    "salary": "string (optional)",
    "address": "string (optional)",
    "created_at": "datetime",
    "updated_at": "datetime (optional)"
}
```

## Security Note

⚠️ **Important**: This implementation stores passwords as plain text for simplicity. In a production environment, you should:
- Hash passwords using bcrypt or similar
- Implement proper authentication tokens (JWT)
- Add input sanitization
- Implement rate limiting
- Use environment variables for connection strings
- Enable MongoDB authentication and SSL
