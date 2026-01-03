# ✅ Solved: "Unauthorized" Error

The issue was a security feature in browsers called **SameSite Cookies**.
*   **The Problem**: Your browser was running on `localhost` but the app was configured to talk to `127.0.0.1`.
*   **The Check**: Browsers treat these as different sites. Because the security setting was "Lax", the browser **refused to send the login cookie** when saving data (POST request), even though it sent it for viewing data (GET request).
*   **The Fix**: I updated the configuration so the App automatically matches your browser's address (e.g., `localhost` to `localhost`).

## 🚀 Final Step
1.  **Logout** completely.
2.  **Hard Refresh** (Very Important!):
    *   Windows: `Ctrl` + `Shift` + `R`
    *   Mac: `Cmd` + `Shift` + `R`
3.  **Login** again.
4.  **Add Transaction**: It will now work because the domains match.

You can verify it works by checking the terminal - you will see "Cookies received: ..." with actual data instead of empty.
