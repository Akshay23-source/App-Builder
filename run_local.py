import os
import sys
import subprocess
import time

def main():
    print("=================================================================")
    print(" Launching ForgeAI Engine & Frontend (Non-Docker Local Mode)")
    print("=================================================================")
    print(" - Backend Gateway API:  http://localhost:8000")
    print(" - Gateway API Docs:     http://localhost:8000/docs")
    print(" - Frontend Web App:     http://localhost:3000")
    print(" - Database:             SQLite (./forgeai.db)")
    print(" - Task Execution:       In-Process Async Worker DAG")
    print("=================================================================")

    backend_cmd = [sys.executable, "-m", "uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    frontend_cmd = ["cmd", "/c", "npm run dev:frontend"] if os.name == "nt" else ["bash", "-c", "npm run dev:frontend"]

    processes = []
    try:
        print("\n[1/2] Starting Backend FastAPI Gateway Service...")
        p_backend = subprocess.Popen(backend_cmd)
        processes.append(p_backend)

        time.sleep(2)

        print("\n[2/2] Starting Next.js Frontend Dev Server...")
        p_frontend = subprocess.Popen(frontend_cmd)
        processes.append(p_frontend)

        print("\n[SUCCESS] ForgeAI services active! Press Ctrl+C to stop.\n")
        
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down ForgeAI services...")
        for p in processes:
            try:
                p.terminate()
            except Exception:
                pass
        print("Done.")

if __name__ == "__main__":
    main()
