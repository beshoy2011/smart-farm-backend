"""
Simple script to run backend without virtual environment issues
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Try to import uvicorn
try:
    import uvicorn
except ImportError:
    print("❌ uvicorn not installed!")
    print("📦 Installing requirements...")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    import uvicorn

# Run server
if __name__ == "__main__":
    print("🚀 Starting Backend on http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("Press Ctrl+C to stop\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


