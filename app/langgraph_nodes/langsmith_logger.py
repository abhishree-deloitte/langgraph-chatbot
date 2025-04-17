# app/langgraph_nodes/langsmith_logger.py

import os
from pathlib import Path
from app.utils.colors import GREEN, CYAN, YELLOW, RESET


def generate_langsmith_log(state: dict):
    print(f"\n{YELLOW}📦 Generating LangSmith trace summary for: {CYAN}{state['project_name']}{RESET}")

    logs_dir = Path("./langsmith_logs")
    logs_dir.mkdir(exist_ok=True)

    project_name = state.get("project_name", "unknown")
    log_path = logs_dir / f"{project_name}_log.txt"

    trace_lines = [
        f"Project: {project_name}",
        f"SRS File: {state.get('file_path')}",
        f"Project Path: {state.get('project_path')}",
        f"Database Setup Success: {state.get('db_init_success')}",
        f"Code Generation Success: {state.get('code_generation_success')}",
        f"Test Passed: {state.get('test_passed')}",
        f"Server Launched: {state.get('server_launched')}",
        f"Docs Generated: {state.get('docs_generated')}",
        f"LLM Calls Made: {state.get('llm_calls', 0)}",
        f"Iterations (for retries): {state.get('iteration_count', 0)}",
        f"Test Output: \n{state.get('test_output', '').strip()[:1000]}..."
    ]

    log_path.write_text("\n".join(trace_lines))
    print(f"{GREEN}✓ LangSmith trace summary {CYAN}{trace_lines}{RESET}\n\n")
    print(f"{GREEN}✓ LangSmith trace saved to: {CYAN}{log_path}{RESET}\n")

    return {
        **state,
        "langsmith_log_path": str(log_path)
    }
