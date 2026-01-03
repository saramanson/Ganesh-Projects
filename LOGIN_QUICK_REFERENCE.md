# Authentication System - Quick Reference

## 🔐 Login URLs

### Web Application
- **Frontend Login Page**: `http://localhost:3000` (auto-redirects to login if not authenticated)
- **Backend Login API**: `http://127.0.0.1:5000/api/auth/login`

### Mobile Application  
- **Frontend**: Same as web (Capacitor handles it)
- **Backend API**: `http://10.0.2.2:5000/api/auth/login` (Android emulator)

## 🚀 Quick Start

### 1. Start the Backend
```bash
cd backend
python app.py
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```

### 3. Create Your First Account
1. Open `http://localhost:3000`
2. Click "Sign up"
3. Enter username, email, and password
4. You're in! 🎉

## 📋 Key Features

✅ **Secure Authentication**
- Bcrypt password hashing
- Session-based login
- Protected API endpoints

✅ **User-Specific Data**
- Each user sees only their own transactions
- Isolated storage per user
- No data leakage between accounts

✅ **Beautiful UI**
- Modern gradient design
- Smooth animations
- Mobile-responsive

## 🔑 Default Test Account

You'll need to create your own account - no default accounts exist for security.

**Minimum Requirements:**
- Username: 3+ characters
- Email: Valid email format
- Password: 6+ characters

## 📱 User Interface

### Login Page
- Username field
- Password field
- "Sign up" link to register

### Register Page
- Username field
- Email field
- Password field
- Confirm password field
- "Sign in" link to login

### Main App (After Login)
- User icon + username in navigation
- Logout button
- All your expense tracking features

## 🛠️ API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/auth/register` | POST | No | Create new account |
| `/api/auth/login` | POST | No | Login to account |
| `/api/auth/logout` | POST | Yes | Logout |
| `/api/auth/check` | GET | No | Check auth status |
| `/api/auth/me` | GET | Yes | Get user info |
| `/api/transactions` | GET | Yes | Get user's transactions |
| `/api/transactions` | POST | Yes | Add transaction |
| `/api/transactions/<id>` | DELETE | Yes | Delete transaction |

## 💡 Tips

1. **Session Persistence**: Your login session persists across page refreshes
2. **Multiple Users**: Each user account is completely isolated
3. **Logout**: Always logout when using shared computers
4. **Password Security**: Use a strong, unique password

## 📖 Full Documentation

For complete details, see: `AUTHENTICATION_GUIDE.md`

---

**Need help?** Check the browser console and backend terminal for error messages.
