import os
from pathlib import Path
from app.utils.colors import GREEN, CYAN, YELLOW, RESET


def store_iteration_node(state):
    """
    Stores a snapshot of the current codebase and error state to `iteration_versions` list.
    This includes:
    - All generated `.py` files under `app/`
    - Any test output if available
    """
    project_path = Path(state["project_path"])
    app_path = project_path / "app"

    code_snapshot = {}
    for file_path in app_path.rglob("*.py"):
        try:
            relative_path = file_path.relative_to(project_path)
            code_snapshot[str(relative_path)] = file_path.read_text()
        except Exception as e:
            print(f"{YELLOW}⚠️ Failed to snapshot {file_path}: {e}{RESET}")

    test_output = state.get("test_output", "")

    snapshot = {
        "iteration": state.get("iteration_count", 0),
        "code_generation_success": state.get("code_generation_success"),
        "test_output": test_output,
        "code_snapshot": code_snapshot,
    }

    versions = state.get("iteration_versions", [])
    iteration_count = state.get("iteration_count", 1)
    versions.append(snapshot)
    print(len(versions))

    print(f"{CYAN}📦 Stored iteration snapshot #{iteration_count} with {len(code_snapshot)} files.{RESET}")

    return {
        **state,
        "iteration_versions": versions,
        "iteration_count": iteration_count + 1,
    }
