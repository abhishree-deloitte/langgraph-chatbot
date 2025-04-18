import os
import re
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from app.utils.colors import GREEN, CYAN, YELLOW, RESET

def generate_code_node(state: dict, model=None):
    print(f"\n{YELLOW}🧬 Generating modular route, service, and schema code...{RESET}")

    if not model:
        model = ChatOpenAI(
            model="llama-3.3-70b-versatile",
            temperature=0.25,
            openai_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_base="https://api.groq.com/openai/v1",
        )

    project_path = Path(state["project_path"])
    models_path = project_path / "app" / "models" / "models.py"
    tests_path = project_path / "tests"

    srs = state["srs_analysis"]
    last_code = state.get("code_snapshot", "")
    models_code = models_path.read_text() if models_path.exists() else "# models.py not found"

    # Optional: Include existing test stubs (if any)
    test_files = []
    if tests_path.exists():
        for file in tests_path.glob("*.py"):
            test_files.append(f"\n# {file.name}\n" + file.read_text())
    test_info = "\n---\nThese are the tests that will be run against your code:\n" + "\n".join(test_files) if test_files else ""

    is_retry = state.get("retrying", False)
    prev_test_output = state.get("test_output", "")

    base_prompt = f"""
You are a professional FastAPI engineer working in a production-grade environment.

You are tasked with generating clean, modular, production-level code for the following folders:
- app/api/routes/
- app/services/
- app/schemas/

The SQLAlchemy models you must build on are:
{models_code}

The system you are building is based on the following Software Requirements:
{srs}

{test_info}

Your tech stack:
- FastAPI
- PostgreSQL (via SQLAlchemy ORM)
- Pydantic for schemas
- Alembic for migrations
- Pytest for testing

❗IMPORTANT:
- All database interaction must use SQLAlchemy ORM
- Use correct DB session patterns (e.g., Dependency Injection if needed)
- Use PostgreSQL-compatible datatypes and logic
- Do NOT generate boilerplate or placeholder logic
- Write real business logic that will pass the tests
- Follow clean code practices, proper naming, separation of concerns
- All return values should be valid, structured, and realistic
- Ensure routes are connected to FastAPI app in `main.py`
- Prefix each router with its appropriate API path:
  - /api/dashboard
  - /api/lms
  - /api/pods
  - /api/auth

Format your response with:
**app/path/to/file.py**
```python
<code>
```
Only include valid code files. No extra text or explanation.
"""

    retry_prompt = f"""
You previously generated code that failed the following tests. You are now being asked to fix only the affected files.

❗Here are the test failures you need to fix:
{prev_test_output.strip()[:2000]}...

The original models were:
{models_code}

The Software Requirements:
{srs}

The current code is:
{last_code}

The error and test output you received was:
{test_info}

✅ Fix only the impacted files and preserve working logic elsewhere. Your output must still follow this format:
**app/path/to/file.py**
```python
<code>
```
Only include valid code files. No extra text or explanation.
"""

    prompt = retry_prompt if is_retry else base_prompt

    response = model([
        SystemMessage(content="You are a professional backend engineer."),
        HumanMessage(content=prompt)
    ])
    lm_calls = state.get("llm_calls", 0) + 1

    # ✅ Match file headers and code blocks using triple backtick syntax
    pattern = r"\*\*(.*?)\*\*\s*```(?:python)?\s*([\s\S]*?)\s*```"
    matches = re.findall(pattern, response.content)

    if not matches:
        print(f"{YELLOW}⚠️ No code blocks matched. LLM may not have followed format.{RESET}")

    for rel_path, code in matches:
        try:
            file_path = project_path / rel_path.strip()
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w") as f:
                f.write(code.strip())
            print(f"{GREEN}  ✓ Generated:{RESET} {CYAN}{file_path}{RESET}")
        except Exception as e:
            print(f"{YELLOW}⚠️ Failed to write {rel_path}: {e}{RESET}")

    return {
        **state,
        "code_generation_success": True,
        "llm_calls": lm_calls,
    }
