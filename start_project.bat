@echo off
echo ==================================================
echo HETHONG WEB TRA CUU NCKH
echo ==================================================
echo.
echo Dang khoi dong Backend API...
start "Backend - FastAPI" cmd /k "cd backend && ..\venv\Scripts\activate && uvicorn app.main:app --port 8000 --reload"

echo Dang khoi dong Frontend Web...
start "Frontend - React Vite" cmd /k "cd frontend\vnu-frontend && npm run dev"

echo.
echo Da mo 2 cua so chay ngam! 
echo Vui long KHONG TAT 2 cua so mau den vung hien thi.
echo Truy cap Web tai: http://localhost:5173
echo.
pause
