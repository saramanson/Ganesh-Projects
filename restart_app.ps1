# restart_app.ps1
# Script to restart the Expense Tracker Application
# It opens new terminal windows for Backend and Frontend so you can monitor them.

$projectDir = "c:\Users\ganea\mygitproject"

Write-Host "Stopping existing services..."
Stop-Process -Name "python" -ErrorAction SilentlyContinue -Force
Stop-Process -Name "node" -ErrorAction SilentlyContinue -Force

Start-Sleep -Seconds 3

Write-Host "Starting Backend (Flask)..."
# cmd /k keeps the window open so you can see logs/errors
Start-Process -FilePath "cmd" -ArgumentList "/k title BACKEND & python app.py" -WorkingDirectory "$projectDir\backend" -WindowStyle Normal

Write-Host "Starting Frontend (Vite)..."
Start-Process -FilePath "cmd" -ArgumentList "/k title FRONTEND & npm run dev" -WorkingDirectory "$projectDir\frontend" -WindowStyle Normal

Write-Host "Done! You should see two new command windows."
