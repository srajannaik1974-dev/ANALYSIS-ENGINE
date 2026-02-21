"""
Start frontend + backend from this project folder.
Run: python start_server.py
Then open http://127.0.0.1:8000 for the UI.
"""
import os
import sys
from pathlib import Path

# Force run from this script's directory so main.py and index.html are found
PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn

PORT = 8001  # Avoid conflict with anything already on 8000

if __name__ == "__main__":
    print("Project folder:", PROJECT_ROOT)
    print("Frontend (input page): http://127.0.0.1:%s" % PORT)
    print("Backend API: http://127.0.0.1:%s/analyze" % PORT)
    print("API docs: http://127.0.0.1:%s/docs" % PORT)
    print("Press Ctrl+C to stop.\n")
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, reload=False)
