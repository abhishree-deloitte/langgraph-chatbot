# Workflow for the project

from langgraph.graph import StateGraph, END
from typing import TypedDict

from app.langgraph_nodes.srs_analysis import analyze_srs_node
from app.langgraph_nodes.project_bootstrap import bootstrap_project_node
from app.langgraph_nodes.db_setup import db_setup_node

class GraphState(TypedDict):
    file_path: str
    project_name: str
    srs_analysis: str
    raw_srs: str
    bootstrap_success: bool
    project_path: str

def build_graph():
    builder = StateGraph(GraphState) 

    builder.add_node("analyze_srs", analyze_srs_node)
    builder.add_node("bootstrap_project", bootstrap_project_node)
    builder.add_node("setup_database", db_setup_node)

    builder.set_entry_point("analyze_srs")
    builder.add_edge("analyze_srs", "bootstrap_project")
    builder.add_edge("bootstrap_project", "setup_database")
    builder.set_finish_point("setup_database")

    return builder.compile()
