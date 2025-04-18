# app/langgraph_nodes/langgraph_visualizer.py

from pathlib import Path
from app.utils.colors import GREEN, YELLOW, CYAN, RESET

def generate_langgraph_docs(state: dict):
    project_name = state["project_name"]
    edges = [
        ("analyze_srs", "bootstrap_project"),
        ("bootstrap_project", "setup_database"),
        ("setup_database", "generate_tests"),
        ("generate_tests", "generate_code"),
        ("generate_code", "execute_code"),
        ("execute_code", "zip_project"),
        ("zip_project", "generate_docs"),
        ("generate_docs", "log_langsmith"),
    ]

    print(f"\n{CYAN}🧩 LangGraph Node Flow (Live Graph):{RESET}")
    for a, b in edges:
        print(f"  {a} ─▶ {b}")

    docs_path = Path("langgraph_docs")
    docs_path.mkdir(exist_ok=True)

    mermaid_file = docs_path / f"{project_name}_langgraph_mermaid.md"
    mermaid_lines = ["```mermaid", "graph TD"]
    for a, b in edges:
        mermaid_lines.append(f"    {a} --> {b}")
    mermaid_lines.append("```")
    mermaid_file.write_text("\n".join(mermaid_lines))
    print(f"{GREEN}  ✓ Mermaid graph written to {mermaid_file}{RESET}")

    dot_file = docs_path / f"{project_name}_langgraph.dot"
    dot_lines = ["digraph G {"]
    for a, b in edges:
        dot_lines.append(f'    "{a}" -> "{b}";')
    dot_lines.append("}")
    dot_file.write_text("\n".join(dot_lines))
    print(f"{GREEN}  ✓ DOT graph written to {dot_file}{RESET}")


    return {
        **state,
        "docs_generated": True
    }
