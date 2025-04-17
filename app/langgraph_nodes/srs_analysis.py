# app/langgraph_nodes/srs_analysis.py

import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from app.utils.docx_parser import extract_text_from_docx
from dotenv import load_dotenv

load_dotenv()


def analyze_srs_node(file_path: str, model=None):
    """
    LangGraph node to analyze the SRS and extract key backend requirements
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY is not set in .env file.")

    if not model:
        model = ChatOpenAI(
            model="llama3-70b-8192",
            temperature=0.2,
            openai_api_key=api_key,
            openai_api_base="https://api.groq.com/openai/v1",
        )

    srs_text = extract_text_from_docx(file_path)

    prompt = f"""
You are a software architect. Analyze the following SRS and extract:

1. List of required API endpoints (methods + paths + parameters)
2. Database schema (tables, fields, relationships)
3. Business logic or rules
4. Authentication and authorization requirements

SRS:
{srs_text}
    """

    response = model([
        SystemMessage(content="You are an expert backend architect."),
        HumanMessage(content=prompt)
    ])

    return {
        "srs_analysis": response.content,
        "raw_srs": srs_text
    }
