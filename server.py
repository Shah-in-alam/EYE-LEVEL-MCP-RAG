import os
from dotenv import load_dotenv
from groundx import GroundX, Document
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("eyelevel-rag")

api_key = os.getenv("GROUNDX_API_KEY")
if not api_key:
    raise ValueError("GROUNDX_API_KEY is missing in .env")

client = GroundX(api_key=api_key)

@mcp.tool()
def search_doc_for_context(query: str) -> str:
    response = client.search.content(
        id=177221,
        query=query,
        n=10
    )
    return str(response)

@mcp.tool()
def ingest_documents(local_file_path: str) -> str:
    file_path = os.path.abspath(local_file_path)
    file_name = os.path.basename(file_path)

    client.ingest(
        documents=[
            Document(
                bucket_id=17279,
                file_name=file_name,
                file_path=file_path,
                file_type="pdf",
                search_data={"key": "value"},
            )
        ]
    )

    return f"Ingested {file_name} into knowledge base. It should be available in a few minutes."

if __name__ == "__main__":
    mcp.run(transport="stdio")