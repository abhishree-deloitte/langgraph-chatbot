# app/langgraph_nodes/code_executor.py

import os
import subprocess
from pathlib import Path
from app.utils.colors import GREEN, RED, YELLOW, CYAN, RESET

def create_conftest(project_path: Path):
    tests_dir = project_path / "tests"
    tests_dir.mkdir(exist_ok=True)
    conftest_file = tests_dir / "conftest.py"

    if not conftest_file.exists():
        conftest_file.write_text("""\
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
""")
        print(f"{GREEN}  ✓ Added Pytest client fixture to:{RESET} {CYAN}{conftest_file}{RESET}")

def install_requirements(project_path: Path):
    print(f"{CYAN}📦 Installing requirements...{RESET}")
    result = subprocess.run("pip install -r requirements.txt", shell=True, cwd=project_path, capture_output=True)
    if result.returncode != 0:
        print(f"{RED}❌ Failed to install requirements:{RESET}\n" + result.stdout.decode() + result.stderr.decode())
    else:
        print(f"{GREEN}✔️ Requirements installed successfully.{RESET}")

def execute_code_node(state):
    print(f"\n{YELLOW}🚀 Running tests and launching FastAPI app for: {CYAN}{state['project_name']}{RESET}")

    project_path = Path(state["project_path"])
    pytest_cmd = "pytest tests"
    uvicorn_cmd = "uvicorn app.main:app --host 0.0.0.0 --port 8000"

    # 🧪 Add test client fixture before testing
    create_conftest(project_path)

    # 📦 Ensure all dependencies are installed
    install_requirements(project_path)

    # ✅ Add PYTHONPATH to environment
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_path.resolve())

    # ✅ Run Pytest
    test_result = subprocess.run(pytest_cmd, shell=True, cwd=project_path, env=env, capture_output=True)
    if test_result.returncode != 0:
        print(f"{RED}❌ Tests failed:{RESET}\n" + test_result.stdout.decode() + test_result.stderr.decode())
        return {
            **state,
            "test_passed": False,
            "test_output": test_result.stdout.decode() + test_result.stderr.decode(),
        }
    else:
        print(f"{GREEN}✔️ Tests passed successfully!{RESET}\n")

    # ✅ Launch FastAPI server (in background)
    print(f"{YELLOW}🌐 Launching server on http://localhost:8000 ...{RESET}")
    subprocess.Popen(uvicorn_cmd, shell=True, cwd=project_path, env=env)

    return {
        **state,
        "test_passed": True,
        "server_launched": True
    }
