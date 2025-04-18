# # main.py
# import os
# from dotenv import load_dotenv
# from app.langgraph_nodes.workflow import build_graph
# from app.utils.colors import YELLOW, CYAN, RESET, GREEN
# from langsmith import Client
# import json
# from uuid import UUID
# from datetime import datetime

# def safe_json(obj):
#     if isinstance(obj, (UUID, datetime)):
#         return str(obj)
#     if isinstance(obj, set):
#         return list(obj)
#     raise TypeError(f"Type {type(obj)} not serializable")

# load_dotenv()

# client = Client()

# if __name__ == "__main__":
#     file_path = "./PythonGenAISRD.docx"

#     print(f"\n{YELLOW}🚀 Starting LangGraph AI Workflow for:{RESET} {CYAN}{file_path}{RESET}")
#     client = Client()
#     runs = list(client.list_runs(limit=1, order_by="desc", project_name=[os.getenv("LANGCHAIN_PROJECT")]))

#     run = runs[0]
#     print(f"{YELLOW}🚀 LangSmith Run ID: {CYAN}{run.id}{RESET}")
#     trace =  client.read_run(run.id).dict()
#     print(json.dumps(trace, indent=2, default=safe_json))
#     print(f"{GREEN}✓ LangSmith trace URL: {CYAN}{trace_url}{RESET}")

#     graph = build_graph()
#     result = graph.invoke({"file_path": file_path})

#     print(f"\n{YELLOW}🏁 Workflow Complete.{RESET} Output written to: {CYAN}generated_projects/{result['project_name']}{RESET}\n")

# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.langgraph_nodes.workflow import build_graph
from app.utils.colors import YELLOW, CYAN, RESET
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from langsmith import Client
import json
from uuid import UUID
from datetime import datetime

def safe_json(obj):
    if isinstance(obj, (UUID, datetime)):
        return str(obj)
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

load_dotenv()

os.makedirs("generated_projects", exist_ok=True)
app = FastAPI(title="Agentic LangGraph Backend")
app.mount("/download", StaticFiles(directory="generated_projects"), name="download")
class FileInput(BaseModel):
    file_path: str

@app.post("/generate-project")
async def generate_project(data: FileInput):
    file_path = data.file_path

    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="File path does not exist.")

    print(f"\n{YELLOW}🚀 Starting LangGraph AI Workflow for:{RESET} {CYAN}{file_path}{RESET}")

    graph = build_graph()
    result = graph.invoke({"file_path": file_path})

    project_name = result["project_name"]
    zip_filename = f"{project_name}.zip"
    zip_path = f"zipped_projects/{zip_filename}"
    download_url = f"http://localhost:8000/download/{zip_filename}"

    # ✅ Fetch LangSmith trace report as JSON
    client = Client()
    runs = list(client.list_runs(limit=1, order_by="desc", project_name=[os.getenv("LANGCHAIN_PROJECT")]))

    if runs:
        try:
            run = runs[0]
            trace = client.read_run(run.id)
            trace_report = trace.dict()
        except Exception as e:
            trace_report = {"error": str(e)}

    return JSONResponse({
        "status": "success",
        "project_name": project_name,
        "zip_file": zip_path,
        "download_link": download_url,
        "langsmith_trace_json": json.dumps(trace_report, indent=2, default=safe_json)
    })

