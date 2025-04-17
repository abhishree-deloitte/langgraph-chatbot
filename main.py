from dotenv import load_dotenv
load_dotenv()

from app.langgraph_nodes.srs_analysis import analyze_srs_node

if __name__ == "__main__":
    file_path = "your_file.docx"  # Replace with your SRS .docx file
    result = analyze_srs_node("./SRS.docx")
    print("\n✅ Extracted SRS Analysis:\n")
    print(result["srs_analysis"])
