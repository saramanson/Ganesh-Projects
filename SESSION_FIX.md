# ✅ Fixed: 405 Error (Session Issue)

The "405 Method Not Allowed" error indicates your **login session has expired**, but the app was trying to redirect you to a page that doesn't exist (because it's an API).

## 🛠️ What I fixed
I updated the backend to properly report **"Unauthorized" (401)** instead of causing a confusing system error.

## 🚀 How to solve it right now
1.  **Logout**: Click the **Logout** button in the top right.
2.  **Login**: Log back in with your credentials (`Ganesh` / `Letmego4awalk`).
3.  **Try Again**: Add your transaction.

It should work perfectly now!
