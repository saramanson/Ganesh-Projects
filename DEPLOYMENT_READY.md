# Deployment Ready!

I have prepared your code for deployment. Because I cannot access your GitHub or Render accounts directly, please follow these steps to put your site online.

## Step 1: Push Code to GitHub

Open a terminal where `git` is installed (e.g., Git Bash or VS Code terminal) and run:

```bash
# 1. Initialize git if you haven't (skip if already done)
git init

# 2. Add all files
git add .

# 3. Commit changes
git commit -m "Prepare for deployment: Update config for environment variables"

# 4. Create a repo on GitHub (https://github.com/new) named 'expense-tracker'

# 5. Connect and push (replace YOUR_USERNAME):
git remote add origin https://github.com/YOUR_USERNAME/expense-tracker.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend (Render)

1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Web Service**.
3. Connect your 'expense-tracker' repo.
4. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**:
     - `PYTHON_VERSION`: `3.11.0`
     - `SECRET_KEY`: (Generate a random string)
     - `ALLOWED_ORIGINS`: `https://YOUR-FRONTEND-URL.onrender.com` (You will update this AFTER Step 3)
5. Click **Create Web Service**.
6. **Copy the Backend URL** (e.g., `https://expense-tracker-backend.onrender.com`).

## Step 3: Deploy Frontend (Render)

1. Click **New +** -> **Static Site**.
2. Connect your 'expense-tracker' repo.
3. Settings:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Environment Variables**:
     - `VITE_API_URL`: Paste your **Backend URL** from Step 2 (e.g., `https://expense-tracker-backend.onrender.com/api`)
     - **Important**: Add `/api` to the end of the URL!
4. Click **Create Static Site**.
5. **Copy the Frontend URL** (e.g., `https://expense-tracker-frontend.onrender.com`).

## Step 4: Final Connection

1. Go back to your **Backend Service** on Render.
2. Go to **Environment** tab.
3. Edit `ALLOWED_ORIGINS`.
4. Set it to your **Frontend URL** (from Step 3).
   - Example: `https://expense-tracker-frontend.onrender.com` (No trailing slash here).
5. Save changes. Render will restart the backend.

## Done!
Visit your Frontend URL. Your app is now live!
