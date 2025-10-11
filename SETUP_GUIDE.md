# Quick Setup Guide

## Your MySQL Configuration
Based on your JDBC string `jdbc:mysql://localhost:3306/?user=root`, I've updated the configuration to match your setup.

## Step 1: Database Setup

### Option A: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Open the `setup_database.sql` file
4. Execute the script to create the database and tables

### Option B: Using MySQL Command Line
```bash
mysql -u root -p
```
Then run:
```sql
source setup_database.sql;
```

## Step 2: Install Python (if not installed)
1. Download Python from https://python.org
2. Make sure to check "Add Python to PATH" during installation
3. Restart your terminal/command prompt

## Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Test Connection
```bash
python test_db_connection.py
```

## Step 5: Initialize Database (Optional)
```bash
python db/init_db.py
```

## Step 6: Start the Server
```bash
python main.py
```

## Your Configuration
- **Database**: `restro_backend`
- **Host**: `localhost`
- **Port**: `3306`
- **User**: `root`
- **Password**: (empty)

## API Endpoints
Once running, you can access:
- **API Docs**: http://localhost:8000/docs
- **Signup**: POST http://localhost:8000/api/v1/auth/signup
- **Login**: POST http://localhost:8000/api/v1/auth/login

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
