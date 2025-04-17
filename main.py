# main.py

from dotenv import load_dotenv
from app.langgraph_nodes.workflow import build_graph
from app.utils.colors import YELLOW, CYAN, RESET

load_dotenv()

if __name__ == "__main__":
    file_path = "./PythonGenAISRD.docx"

    print(f"\n{YELLOW}🚀 Starting LangGraph AI Workflow for:{RESET} {CYAN}{file_path}{RESET}")

    graph = build_graph()
    result = graph.invoke({"file_path": file_path})

    print(f"\n{YELLOW}🏁 Workflow Complete.{RESET} Output written to: {CYAN}generated_projects/{result['project_name']}{RESET}\n")
