# 🚀 How to Run the Application

This guide explains how to start the backend and frontend servers yourself. You will need two separate terminal/command prompt windows.

## ✅ Prerequisites

Ensure you have the following installed:
*   **Python** (for the backend)
*   **Node.js** (for the frontend)

---

## 1️⃣ Start the Backend

1.  Open a **new terminal**.
2.  Navigate to the `backend` folder:
    ```powershell
    cd backend
    ```
3.  Run the application:
    ```powershell
    python app.py
    ```
4.  You should see output indicating the server is running on `http://127.0.0.1:5000`.

---

## 2️⃣ Start the Frontend

1.  Open a **second terminal**.
2.  Navigate to the `frontend` folder:
    ```powershell
    cd frontend
    ```
3.  Run the development server.
    *   **Standard command:**
        ```powershell
        npm run dev
        ```
    *   **If you get a "scripts is disabled" error**, use this command instead:
        ```powershell
        powershell -ExecutionPolicy Bypass -Command "npm run dev"
        ```
4.  You should see output like:
    ```
    ➜  Local:   http://localhost:5173/
    ```

---

## 3️⃣ Access the Application

Open your web browser and go to:

👉 **[http://localhost:5173](http://localhost:5173)**

*   **Login**: Use your created account (e.g., username `Ganesh`).
*   **Important**: Do **not** use port 3000. The correct port is **5173**.

---

## ❓ Troubleshooting

### "Port already in use"
If you see an error saying a port is busy:
1.  Close the terminal window where the previous server was running.
2.  Or, task manager -> End Task for `python` or `node` processes.

### "Module not found" (Backend)
If you get an error about missing modules:
```powershell
pip install -r requirements.txt
```

### "Vite not found" or similar (Frontend)
If `npm run dev` fails with missing packages:
```powershell
npm install
```
