@echo off
echo 🐾 PetLink Pet Adoption System
echo ================================
echo.
echo Installing Flask if needed...
pip install flask
echo.
echo Starting PetLink application...
echo.
echo 📍 Application URLs:
echo    🌐 Main site: http://localhost:5000
echo    🔑 Owner login: http://localhost:5000/owner-login
echo    📧 Demo: admin@petlink.com / admin123
echo.
echo Press Ctrl+C to stop the application
echo.
python app_fixed.py
pause