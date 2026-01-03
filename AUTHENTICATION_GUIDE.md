# Authentication System Documentation

## Overview
Your Expense Tracker now has a complete user authentication system with login, registration, and user-specific data isolation.

## Features Implemented

### Backend (Flask)
1. **User Authentication Module** (`backend/auth.py`)
   - User registration with email and password
   - Secure password hashing using bcrypt
   - Login/logout functionality
   - Session management with Flask-Login
   - SQLite database for user storage

2. **Protected API Endpoints**
   - All transaction endpoints now require authentication
   - User-specific data storage (each user only sees their own transactions)
   - Automatic session validation

3. **Database Structure**
   - `users.db` - Stores user accounts (id, username, email, password_hash, created_at)
   - User-specific transaction folders: `storage/user_{id}/`

### Frontend (React)
1. **Authentication Components**
   - `Login.jsx` - Beautiful login form
   - `Register.jsx` - User registration form
   - `Auth.css` - Modern, gradient-based styling

2. **Authentication Flow**
   - Auto-check authentication on app load
   - Redirect to login if not authenticated
   - Display user info and logout button when logged in
   - Seamless transition between login and register views

3. **API Integration**
   - Axios configured to send credentials (cookies)
   - Authentication API functions (login, register, logout, checkAuth)
   - Error handling for authentication failures

## API Endpoints

### Authentication Endpoints

#### POST `/api/auth/register`
Register a new user account.

**Request Body:**
```json
{
  "username": "string (min 3 chars)",
  "email": "string (valid email)",
  "password": "string (min 6 chars)"
}
```

**Response (201):**
```json
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### POST `/api/auth/login`
Login with existing credentials.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### POST `/api/auth/logout`
Logout current user (requires authentication).

**Response (200):**
```json
{
  "message": "Logout successful"
}
```

#### GET `/api/auth/check`
Check if user is authenticated.

**Response (200):**
```json
{
  "authenticated": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### GET `/api/auth/me`
Get current user info (requires authentication).

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### Protected Transaction Endpoints

All transaction endpoints now require authentication:
- `GET /api/transactions` - Get user's transactions
- `POST /api/transactions` - Add new transaction
- `DELETE /api/transactions/<id>` - Delete transaction

## Login URL

### For Web Application:
- **Frontend URL**: `http://localhost:3000` (or your React dev server port)
- **Login Page**: Automatically shown when not authenticated
- **Backend API**: `http://127.0.0.1:5000/api/auth/login`

### For Mobile Application:
- **Frontend**: Same as web (Capacitor handles routing)
- **Backend API**: `http://10.0.2.2:5000/api/auth/login` (Android emulator)
- Or your computer's local IP for physical devices

## Usage Instructions

### Starting the Application

1. **Start Backend:**
   ```bash
   cd backend
   python app.py
   ```
   Backend runs on: `http://127.0.0.1:5000`

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend runs on: `http://localhost:3000` (or similar)

3. **First Time Setup:**
   - Navigate to the frontend URL
   - You'll see the login page
   - Click "Sign up" to create a new account
   - Fill in username, email, and password
   - After registration, you'll be automatically logged in

### User Experience Flow

1. **New User:**
   - Opens app → Sees login page
   - Clicks "Sign up" → Registration form
   - Enters details → Account created → Logged in automatically
   - Can now add/view transactions

2. **Returning User:**
   - Opens app → Sees login page
   - Enters credentials → Logged in
   - Sees their own transactions only

3. **Logged In User:**
   - Can switch between Expense Tracker and Split Expenses
   - Username displayed in navigation bar
   - Click "Logout" to sign out

## Security Features

1. **Password Security:**
   - Passwords hashed with bcrypt (industry standard)
   - Never stored in plain text
   - Minimum 6 characters required

2. **Session Management:**
   - Flask-Login handles sessions securely
   - Session cookies with proper configuration
   - Automatic session validation on each request

3. **Data Isolation:**
   - Each user has separate storage directory
   - Users can only access their own transactions
   - API endpoints validate user ownership

4. **Input Validation:**
   - Username: minimum 3 characters
   - Email: valid email format required
   - Password: minimum 6 characters
   - Duplicate username/email prevention

## File Structure

```
backend/
├── app.py                 # Main Flask app with protected routes
├── auth.py               # Authentication module
├── users.db              # User database (auto-created)
├── storage/
│   ├── user_1/          # User 1's transactions
│   │   ├── 2024/
│   │   └── 2025/
│   └── user_2/          # User 2's transactions
│       ├── 2024/
│       └── 2025/

frontend/
├── src/
│   ├── App.jsx          # Main app with auth logic
│   ├── api.js           # API functions including auth
│   └── components/
│       ├── Login.jsx    # Login component
│       ├── Register.jsx # Registration component
│       └── Auth.css     # Authentication styling
```

## Configuration

### Backend Configuration (app.py)

```python
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
```

**Important for Production:**
- Change `SECRET_KEY` to a random, secure value
- Set `SESSION_COOKIE_SECURE = True` when using HTTPS
- Update CORS origins to your production domain

### Frontend Configuration (api.js)

```javascript
axios.defaults.withCredentials = true;
```

This ensures cookies are sent with every request.

## Troubleshooting

### Issue: "Login failed" or "Registration failed"
- Check backend is running on port 5000
- Verify frontend can reach backend (check console for CORS errors)
- Ensure credentials are correct

### Issue: "Not authenticated" errors
- Clear browser cookies and try logging in again
- Check that `axios.defaults.withCredentials = true` is set
- Verify CORS configuration allows credentials

### Issue: Can't see transactions after login
- Check browser console for API errors
- Verify user is authenticated (check `/api/auth/check`)
- Ensure transactions are being created in user-specific folder

### Issue: Session expires too quickly
- Flask-Login sessions are permanent by default
- Check browser isn't blocking cookies
- Verify SECRET_KEY is set in Flask config

## Testing the System

### Manual Testing Steps:

1. **Test Registration:**
   - Open app → Click "Sign up"
   - Enter: username="testuser", email="test@example.com", password="test123"
   - Should redirect to main app after successful registration

2. **Test Login:**
   - Logout → Click "Sign in"
   - Enter credentials from step 1
   - Should see main app with transactions

3. **Test Data Isolation:**
   - Create account A, add some transactions
   - Logout, create account B, add different transactions
   - Verify each user only sees their own data

4. **Test Session Persistence:**
   - Login → Add transaction → Refresh page
   - Should remain logged in and see transactions

## Next Steps / Enhancements

Potential improvements you could add:

1. **Password Reset:** Email-based password recovery
2. **Remember Me:** Optional persistent login
3. **Profile Management:** Edit username, email, password
4. **Email Verification:** Verify email addresses
5. **OAuth:** Login with Google, Facebook, etc.
6. **Two-Factor Auth:** Additional security layer
7. **Account Deletion:** Allow users to delete their account
8. **Admin Panel:** Manage users (if needed)

## Support

If you need help with the authentication system:
1. Check the browser console for errors
2. Check the backend terminal for error messages
3. Verify all dependencies are installed
4. Ensure both frontend and backend are running

---

**Created:** January 1, 2026
**Version:** 1.0
