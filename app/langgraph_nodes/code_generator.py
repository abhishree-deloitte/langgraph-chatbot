# app/langgraph_nodes/code_generator.py

import os
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from app.utils.colors import GREEN, CYAN, YELLOW, RESET

def generate_code_node(state: dict, model=None):
    print(f"\n{YELLOW}🧬 Generating modular route, service, and schema code...{RESET}")

    if not model:
        model = ChatOpenAI(
            model="llama3-70b-8192",
            temperature=0.25,
            openai_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_base="https://api.groq.com/openai/v1",
        )

    project_path = Path(state["project_path"])
    api_dir = project_path / "app" / "api" / "routes"
    service_dir = project_path / "app" / "services"
    schema_dir = project_path / "app" / "schemas"

    api_dir.mkdir(parents=True, exist_ok=True)
    service_dir.mkdir(parents=True, exist_ok=True)
    schema_dir.mkdir(parents=True, exist_ok=True)

    srs = state["srs_analysis"]

    base_prompt = f"""
You are a senior backend engineer working with FastAPI.
Based on the following API design, generate code for:
1. FastAPI route handlers (in app/api/routes/)
2. Business logic as services (in app/services/)
3. Request/response Pydantic schemas (in app/schemas/)

Do NOT include markdown or triple backticks.
Only return Python code, and split each section clearly with a marker like:
# === FILE: app/api/routes/leave_routes.py ===
<code>

API Design:
{srs}
"""

    response = model([
        SystemMessage(content="You are a professional backend engineer."),
        HumanMessage(content=base_prompt)
    ])

    code_blocks = response.content.split("# === FILE:")

    for block in code_blocks:
        if not block.strip():
            continue
        try:
            header, code = block.strip().split("===", 1)
            rel_path = header.strip()
            file_path = project_path / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w") as f:
                f.write(code.strip())
            print(f"{GREEN}  ✓ Generated:{RESET} {CYAN}{file_path}{RESET}")
        except Exception as e:
            print(f"{CYAN}⚠️ Skipping malformed block: {e}{RESET}")

    return {
        **state,
        "code_generation_success": True
    }