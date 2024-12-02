import os
import logging
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core.settings import Settings

from mcp_rag.data_dir import get_data_dir

def create_index():
    try:
        # Load the documents
        documents = SimpleDirectoryReader(os.getenv("FOLDER_PATH")).load_data()

        embed_model = OpenAIEmbedding(
            model="text-embedding-3-large",
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # embed_model = AzureOpenAIEmbedding(
        #     model="text-embedding-3-large",
        #     deployment_name="<deployment_name>",
        #     api_key=os.getenv("OPENAI_API_KEY"),
        #     azure_endpoint=os.getenv("OPENAI_API_BASE"),
        #     api_version=os.getenv("OPENAI_API_VERSION"),
        # )

        Settings.embed_model = embed_model

        # Create the index
        index = VectorStoreIndex.from_documents(documents)

        # Save the index
        index.storage_context.persist(persist_dir= get_data_dir() / "index")
    except:
        logging.error(f"Error creating index", exc_info=True)
        path = get_data_dir() / "index"
        if os.path.exists(path):
            os.rmdir(path)