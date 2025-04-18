# main.py

# from dotenv import load_dotenv
# from app.langgraph_nodes.workflow import build_graph
# from app.utils.colors import YELLOW, CYAN, RESET

# load_dotenv()

# if __name__ == "__main__":
#     file_path = "./PythonGenAISRD.docx"

#     print(f"\n{YELLOW}🚀 Starting LangGraph AI Workflow for:{RESET} {CYAN}{file_path}{RESET}")

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

load_dotenv()

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
    zip_path = f"generated_projects/{zip_filename}"

    download_url = f"http://localhost:8000/download/{zip_filename}"

    return JSONResponse({
        "status": "success",
        "project_name": project_name,
        "zip_file": zip_path,
        "download_link": download_url,
    })
