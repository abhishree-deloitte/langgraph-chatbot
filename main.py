from dotenv import load_dotenv
load_dotenv()

from app.langgraph_nodes.workflow import build_graph

if __name__ == "__main__":
    file_path = "./PythonGenAISRD.docx"  

    graph = build_graph()
    result = graph.invoke({"file_path": file_path})

    print("\n✅ Final Graph State:\n")
    for k, v in result.items():
        print(f"{k}: {v}")
