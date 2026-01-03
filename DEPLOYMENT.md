# Deployment Guide - Expense Tracker

This guide will help you deploy your Expense Tracker application to the web for free.

## Option 1: Render (Recommended - Free & Easy)

Render offers free hosting for both frontend and backend.

### Prerequisites
1. Create a GitHub account (if you don't have one): https://github.com
2. Create a Render account: https://render.com (sign up with GitHub)

### Step 1: Push Code to GitHub

1. **Initialize Git in your project** (if not already done):
```bash
cd c:/Users/ganea/Antigravity
git init
git add .
git commit -m "Initial commit - Expense Tracker"
```

2. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Name it "expense-tracker"
   - Don't initialize with README
   - Click "Create repository"

3. **Push your code**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/expense-tracker.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend to Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: expense-tracker-backend
   - **Root Directory**: backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free
5. Add Environment Variable:
   - Key: `PYTHON_VERSION`
   - Value: `3.11.0`
6. Click "Create Web Service"
7. **Copy the URL** (e.g., https://expense-tracker-backend.onrender.com)

### Step 3: Update Frontend API URL

Before deploying frontend, update the API URL:

1. Edit `frontend/src/api.js`:
```javascript
const API_URL = 'https://YOUR-BACKEND-URL.onrender.com/api';
```

2. Commit and push:
```bash
git add frontend/src/api.js
git commit -m "Update API URL for production"
git push
```

### Step 4: Deploy Frontend to Render

1. In Render dashboard, click "New +" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - **Name**: expense-tracker-frontend
   - **Root Directory**: frontend
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: dist
4. Click "Create Static Site"
5. **Your app will be live at**: https://expense-tracker-frontend.onrender.com

### Step 5: Update CORS in Backend

Update `backend/app.py` to allow your frontend domain:
```python
CORS(app, origins=["https://expense-tracker-frontend.onrender.com"])
```

Commit and push - Render will auto-deploy.

---

## Option 2: Vercel (Frontend) + Render (Backend)

### Backend: Same as above (Render)

### Frontend: Vercel
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New" → "Project"
4. Import your GitHub repository
5. Configure:
   - **Root Directory**: frontend
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: dist
6. Add Environment Variable:
   - `VITE_API_URL`: Your backend URL
7. Deploy!

---

## Important Notes

### Backend Considerations
- **Free tier limitations**: Render free tier spins down after 15 minutes of inactivity
- **First request**: May take 30-60 seconds to wake up
- **Storage**: Files are ephemeral on free tier - consider upgrading or using cloud storage (AWS S3, Cloudinary) for images

### Production Improvements Needed

1. **Add gunicorn** to `backend/requirements.txt`:
```
flask
flask-cors
gunicorn
```

2. **Environment Variables**: Create `.env` files for sensitive data

3. **Database**: Consider PostgreSQL for production instead of JSON files

4. **Image Storage**: Use cloud storage (AWS S3, Cloudinary) instead of local files

---

## Quick Test Locally First

Before deploying, test the production build locally:

**Backend:**
```bash
cd backend
pip install gunicorn
gunicorn app:app
```

**Frontend:**
```bash
cd frontend
npm run build
npm run preview
```

---

## Need Help?

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs

Your app will be accessible via a public URL once deployed!
