# 🩺 Troubleshooting: "Saving" Issues

I have added advanced debugging and logic to solve the saving issue.

## 1. 🔍 Diagnosis
The "not saving" issue is likely one of two things:
1.  **Format Error**: Typing `$` or `,` in the amount field (Fixed: I now strip these automatically).
2.  **Visibility Error**: You add a 2026 expense, but the view is stuck on 2025. (Fixed: I now **automatically switch** the view to the year of your new transaction).

## 2. 🛠️ Action Required
Please perform a **Hard Refresh** to ensure you have the latest code:
*   **Windows**: Press `Ctrl` + `Shift` + `R` (or `Ctrl` + `F5`).
*   **Mac**: Press `Cmd` + `Shift` + `R`.

## 3. 🧪 Verify with Debug Logs
If it still fails, check the **Terminal** where you are running the backend (`python app.py`).
*   You will now see messages like:
    ```
    DEBUG: Received add_transaction request...
    DEBUG: Successfully saved transaction...
    ```
*   If you see "Error saving transaction", please tell me the error message.

## 4. 📝 Try adding this exact example:
*   **Description**: Car Insurance
*   **Amount**: 1125 (You can type 1125$ now, it will be cleaned)
*   **Date**: Select Jan 2nd, 2026
*   **Category**: Insurance

Result: It should appear immediately at the top of the list, and the year filter should jump to 2026.
