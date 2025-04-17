# node 4

import os
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from app.utils.colors import GREEN, CYAN, YELLOW, RESET


def generate_tests_node(state: dict, model=None):
    print(f"\n{YELLOW}🧪 Generating unit tests for FastAPI routes...{RESET}")

    if not model:
        model = ChatOpenAI(
            model="llama3-70b-8192",
            temperature=0.3,
            openai_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_base="https://api.groq.com/openai/v1",
        )

    srs_summary = state["srs_analysis"]
    project_path = Path(state["project_path"])
    test_path = project_path / "tests"
    test_path.mkdir(parents=True, exist_ok=True)

    prompt = f"""
You are a senior Python developer.
Based on the following API design description, write pytest-based unit tests
for the FastAPI endpoints. Place each test case in its own function.

Use standard FastAPI TestClient, and assume needed imports.
Return only valid Python code, no markdown or comments.

Return only valid Python code. Do not include markdown, triple backticks, or explanatory comments.

API Summary:
{srs_summary}
    """

    response = model([
        SystemMessage(content="You are an expert in Python API testing."),
        HumanMessage(content=prompt)
    ])

    test_file = test_path / "test_routes.py"
    with open(test_file, "w") as f:
        f.write(response.content)

    print(f"{GREEN}  ✓ Test file written at: {CYAN}{test_file}{RESET}")

    return {
        **state,
        "tests_generated": True,
        "test_file": str(test_file)
    }
