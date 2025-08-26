#!/usr/bin/env python3
"""
PetLink Startup Script
This script will check dependencies and start the PetLink application
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_flask():
    """Install Flask if not available"""
    try:
        import flask
        print(f"✅ Flask {flask.__version__} - Already installed")
        return True
    except ImportError:
        print("📦 Installing Flask...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("✅ Flask installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Flask")
            print("Please run: pip install flask")
            return False

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app_fixed.py',
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/register.html',
        'templates/owner_login.html',
        'templates/profile.html',
        'templates/adopt.html',
        'templates/owner_dashboard.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files present")
    return True

def start_application():
    """Start the PetLink application"""
    print("\n" + "="*60)
    print("🐾 STARTING PETLINK APPLICATION")
    print("="*60)
    
    try:
        # Import and run the application
        os.system('python app_fixed.py')
    except KeyboardInterrupt:
        print("\n\n👋 PetLink application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

def main():
    print("🐾 PetLink Application Startup")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install Flask if needed
    if not install_flask():
        return
    
    # Check required files
    if not check_files():
        return
    
    print("\n✅ All checks passed!")
    print("\n📍 Application will be available at:")
    print("   🌐 Main site: http://localhost:5000")
    print("   🔑 Owner login: http://localhost:5000/owner-login")
    print("   📧 Demo credentials: admin@petlink.com / admin123")
    
    input("\nPress Enter to start the application...")
    start_application()

if __name__ == "__main__":
    main()