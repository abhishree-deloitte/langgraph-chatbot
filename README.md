# LangGraph FastAPI Agent

An **autonomous agent** powered by **LangGraph**, **Llama 3**, and **FastAPI** that takes a `.docx` SRS (Software Requirements Specification) file as input and builds a complete production-grade backend project, including:

- 📂 FastAPI boilerplate project structure
- 🧠 SRS analysis with LLM to extract endpoints, DB schema, and logic
- 🗃️ PostgreSQL setup with SQLAlchemy and Alembic migrations
- 🧪 Unit test generation (Test-Driven Development)
- 🧬 Full CRUD route, service, schema generation
- ✅ Pytest execution & auto-debugging (WIP)
- 🌐 API server launch + OpenAPI spec
- 📦 Zipped project output
- 📊 LangGraph + LangSmith logging & visualization

---

## 📌 How it Works

1. Upload a `.docx` SRS file
2. The LangGraph workflow kicks off:
   - Parses SRS using LLM
   - Extracts project name
   - Bootstraps project fold    # 📄 DOT fileer inside `/generated_projects/<project_name>`
   - Sets up PostgreSQL container using Podman
   - Generates SQLAlchemy models & Alembic migrations
   - Generates schemas, routes, and services based on extracted logic
   - Runs tests and launches the API server
   - Generates zip, documentation, and LangGraph Mermaid + LangSmith logs
3. Returns:
   - A downloadable zip file
   - A detailed LangSmith trace report in JSON format

---

## 🚀 Getting Started

### 🧰 Prerequisites
- Python 3.12+
- Podman (Docker alternative)
- Linux Mint Cinnamon (dev environment) or compatible Linux distro
- Git + Make
- LangSmith account & API Key

### 🔧 Installation
```bash
git clone https://github.com/abhishree-deloitte/langgraph-chatbot.git
cd langgraph-chatbot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the root:
```env
GROQ_API_KEY=your_groq_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=FastAPIAgent
```

### 🏃‍♂️ Run the Agent
```bash
uvicorn app.agent_api:app --reload
```
Visit: `http://localhost:8000/docs` to try the API.

Or run manually:
```bash
python main.py
```

---

## 🔁 LangGraph Workflow
```
[SRS Input] → [Node 1: SRS Analysis]
           → [Node 2: Bootstrap Project]
           → [Node 3: Setup PostgreSQL + Alembic]
           → [Node 4: TDD Unit Tests]
           → [Node 5: Code Generation]
           → [Node 6: Code Execution + Tests + Server]
           → [Node 7: Iteration Memory (WIP)]
           → [Node 8: Zipping + Documentation]
           → [Node 9: LangGraph Visualization]
           → [Node 10: LangSmith Reporting]
           → [Zip + JSON Output]
```

---

## 📁 Output Example

- `/generated_projects/<project_name>/`
  - `app/main.py` ✅
  - `app/models/models.py` ✅
  - `app/services/` ✅
  - `app/api/routes/` ✅
  - `app/schemas/` ✅
  - `alembic/` ✅
  - `tests/test_routes.py` ✅
  - `Dockerfile`, `.env`, `README.md`, etc ✅

---

## 📊 Logs & Monitoring
- `langsmith_logs/<project>_trace.json` : Full execution trace
- `README.md` : Updated with Mermaid LangGraph and token usage
- `zipped_projects/<project>.zip` : Final downloadable output

---

## 📦 Deployment
This project is meant to be easily deployable inside any secure internal infrastructure, or expose a Swagger-based endpoint for secure public usage.

---

## 🧠 Powered By
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Llama 3](https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct)
- [LangSmith](https://smith.langchain.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Podman](https://podman.io/)

---

## 👩‍💻 Author
**Abhishree**  
Built at [HashedIn by Deloitte] with ❤️