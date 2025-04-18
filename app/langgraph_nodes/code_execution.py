# node 6 

import os
import subprocess
from pathlib import Path
from app.utils.colors import GREEN, RED, YELLOW, CYAN, RESET

def create_conftest(project_path: Path):
    tests_dir = project_path / "tests"
    tests_dir.mkdir(exist_ok=True)
    conftest_file = tests_dir / "conftest.py"

    if not conftest_file.exists():
        conftest_file.write_text("""\nimport sys\nimport os\nsys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))\n\nimport pytest\nfrom fastapi.testclient import TestClient\nfrom app.main import app\n\n@pytest.fixture\ndef client():\n    return TestClient(app)\n""")
        print(f"{GREEN}  ✓ Added Pytest client fixture to:{RESET} {CYAN}{conftest_file}{RESET}")

def install_requirements(project_path: Path):
    print(f"{CYAN}📦 Installing requirements...{RESET}")
    result = subprocess.run("pip install -r requirements.txt", shell=True, cwd=project_path, capture_output=True)
    if result.returncode != 0:
        print(f"{RED}❌ Failed to install requirements:{RESET}\n" + result.stdout.decode() + result.stderr.decode())
    else:
        print(f"{GREEN}✔️ Requirements installed successfully.{RESET}")

def run_tests_node(state):
    print(f"\n{YELLOW}🧪 Running tests only for: {CYAN}{state['project_name']}{RESET}")

    project_path = Path(state["project_path"])
    pytest_cmd = "pytest tests"

    create_conftest(project_path)
    install_requirements(project_path)

    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_path.resolve())

    test_result = subprocess.run(pytest_cmd, shell=True, cwd=project_path, env=env, capture_output=True)
    test_output = test_result.stdout.decode() + test_result.stderr.decode()

    if test_result.returncode != 0:
        print(f"{RED}❌ Tests failed:{RESET}\n" + test_output)
        return {
            **state,
            "test_passed": False,
            "test_output": test_output,
            "retrying": True,
        }
    else:
        print(f"{GREEN}✔️ Tests passed successfully!{RESET}\n")
        return {
            **state,
            "test_passed": True,
            "test_output": test_output,
            "retrying": False,
        }
