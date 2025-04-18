# app/langgraph_nodes/code_launcher.py

import os
import subprocess
import webbrowser
from pathlib import Path
from app.utils.colors import GREEN, CYAN, YELLOW, RESET

def launch_code_node(state):
    print(f"\n{YELLOW}🚀 Launching final FastAPI app for: {CYAN}{state['project_name']}{RESET}")

    project_path = Path(state["project_path"])
    port = 8001  # different from model port
    uvicorn_cmd = f"uvicorn app.main:app --host 0.0.0.0 --port {port}"

    # ✅ Add PYTHONPATH to environment
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_path.resolve())

    subprocess.Popen(uvicorn_cmd, shell=True, cwd=project_path, env=env)
    print(f"{GREEN}✔️ FastAPI app running on http://localhost:{port}{RESET}")

    try:
        swagger_url = f"http://localhost:{port}/docs"
        webbrowser.open_new_tab(swagger_url)
        print(f"{CYAN}🔗 Opened Swagger UI in browser: {swagger_url}{RESET}")
    except Exception as e:
        print(f"{YELLOW}⚠️ Could not open browser: {e}{RESET}")

    return {
        **state,
        "server_launched": True
    }
