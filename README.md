# Restro Backend

A restaurant backend API built with FastAPI, featuring user authentication and role-based access control.

## Features

- 🔐 JWT-based authentication
- 👥 Role-based access control (Admin, Employee, Customer)
- 🗄️ MySQL database integration
- 📝 Customer signup and user login
- 🛡️ Password hashing and security
- 📚 Auto-generated API documentation

## User Roles

- **Admin**: Full system access
- **Employee**: Limited access for restaurant staff
- **Customer**: Customer access (only role that can sign up)

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed
2. **MySQL Server** running
3. **MySQL Workbench** (optional, for database management)

### Database Setup

1. Create a MySQL database named `restro_backend`:
   ```sql
   CREATE DATABASE restro_backend;
   ```

2. Update database credentials in `.env` file:
   ```
   DATABASE_URL=mysql+pymysql://your_username:your_password@localhost:3306/restro_backend
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=restro_backend
   ```

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Test database connection**:
   ```bash
   python test_db_connection.py
   ```

3. **Initialize database** (creates tables and default roles):
   ```bash
   python db/init_db.py
   ```

4. **Start the server**:
   ```bash
   python main.py
   ```
   or
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Customer registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info
- `GET /api/v1/auth/profile` - Get user profile

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Default Admin User

After running `python db/init_db.py`, a default admin user is created:
- **Email**: admin@restro.com
- **Password**: admin123

## Development

The project structure:
```
restro_backend/
├── app/           # Application logic and schemas
├── db/            # Database models and connection
├── routes/        # API routes
├── endpoints/     # API endpoints
├── main.py        # FastAPI application
├── config.py      # Configuration settings
└── requirements.txt
```

## Security Notes

- Change the `SECRET_KEY` in `.env` for production
- Use strong passwords in production
- Enable HTTPS in production
- Regularly update dependencies
