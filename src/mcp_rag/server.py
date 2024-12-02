import logging
import os
from collections.abc import Sequence

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding

from mcp_rag.create_index import create_index
from mcp_rag.data_dir import get_data_dir

app = Server("mcp-rag")
retriever = None

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools for retrieving data"""
    return [
        types.Tool(
            name="retrieve",
            description="Retrieve data based on the query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query to retrieve data"
                    }   
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: types.Any) -> Sequence[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for retrieving data"""
    global retriever
    if name != "retrieve":
        raise ValueError(f"Unknown tool: {name}")

    if not isinstance(arguments, dict) or "query" not in arguments:
        raise ValueError("Invalid retrieve arguments")

    query = arguments["query"]

    try:
        docs = retriever.retrieve(query)

        response = ""
        for doc in docs:
            response += doc.text + "\n\n"

        return [
            types.TextContent(
                type="text",
                text=response
            )
        ]
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise RuntimeError(f"Error: {str(e)}")

# Start server
async def main():
    global retriever

    data_dir = get_data_dir()

    index_available = False
    index_dir = data_dir / "index"
    if index_dir.exists():
        for file in index_dir.glob("*.json"):
            if file.name == "docstore.json":
                index_available = True
                break

    if not index_available:
        create_index()
    
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=data_dir / "index")

    # load index
    index = load_index_from_storage(storage_context)

    embed_model = OpenAIEmbedding(
        model="text-embedding-3-large",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # embed_model = AzureOpenAIEmbedding(
    #     model="text-embedding-3-large",
    #     deployment_name="text-embedding-3-large",
    #     api_key=os.getenv("OPENAI_API_KEY"),
    #     azure_endpoint=os.getenv("OPENAI_API_BASE"),
    #     api_version=os.getenv("OPENAI_API_VERSION"),
    # )

    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
        embed_model=embed_model,
    )
    
    async with stdio_server() as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options()
        )