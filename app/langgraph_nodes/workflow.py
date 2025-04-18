# Workflow for the project

from langgraph.graph import StateGraph, END
from typing import TypedDict

from app.langgraph_nodes.srs_analysis import analyze_srs_node
from app.langgraph_nodes.project_bootstrap import bootstrap_project_node
from app.langgraph_nodes.db_setup import db_setup_node
from app.langgraph_nodes.test_generator import generate_tests_node
from app.langgraph_nodes.code_generator import generate_code_node
from app.langgraph_nodes.code_execution import run_tests_node
from app.langgraph_nodes.zip_packager import zip_and_document_node
from app.langgraph_nodes.langgraph_visualizer import generate_langgraph_docs
from app.langgraph_nodes.langsmith_logger import generate_langsmith_log
from app.langgraph_nodes.iteration_memory import store_iteration_node

class GraphState(TypedDict):
    file_path: str
    project_name: str
    srs_analysis: str
    raw_srs: str
    bootstrap_success: bool
    project_path: str
    db_init_success: bool
    test_passed: bool
    server_launched: bool
    docs_generated: bool
    code_generation_success: bool
    langsmith_log_path: str
    iteration_count: int
    llm_calls: int
    test_output: str
    retrying: bool

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("analyze_srs", analyze_srs_node)
    builder.add_node("bootstrap_project", bootstrap_project_node)
    builder.add_node("setup_database", db_setup_node)
    builder.add_node("generate_tests", generate_tests_node)
    builder.add_node("generate_code", generate_code_node)
    builder.add_node("execute_code", run_tests_node)
    builder.add_node("store_iteration", store_iteration_node)
    builder.add_node("zip_project", zip_and_document_node)
    builder.add_node("generate_docs", generate_langgraph_docs)
    builder.add_node("log_langsmith", generate_langsmith_log)

    # Edges
    builder.set_entry_point("analyze_srs")
    builder.add_edge("analyze_srs", "bootstrap_project")
    builder.add_edge("bootstrap_project", "setup_database")
    builder.add_edge("setup_database", "generate_tests")
    builder.add_edge("generate_tests", "generate_code")
    builder.add_edge("generate_code", "execute_code")

    # Conditional Flow Based on Test Result
    def handle_test_result(state: GraphState):
        if state.get("test_passed"):
            return "passed"
        elif state.get("iteration_count", 0) < 5:
            return "failed"
        else:
            return "passed" # End the loop if too many iterations and proceed with errors

    builder.add_conditional_edges("execute_code", handle_test_result, {
        "passed": "zip_project",
        "failed": "store_iteration",
    })

    builder.add_edge("store_iteration", "generate_code")  # Loop back
    builder.add_edge("zip_project", "generate_docs")
    builder.add_edge("generate_docs", "log_langsmith")
    builder.set_finish_point("log_langsmith")

    return builder.compile()