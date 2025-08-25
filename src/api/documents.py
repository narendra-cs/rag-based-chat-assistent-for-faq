import os
from fastapi import APIRouter, HTTPException, status
from langchain_openai.embeddings import OpenAIEmbeddings

from src.common.vector_store import VectorStore
from src.common.document_loader import load_documents
from src.common.utils import ProductEnum, get_logger, load_env


logger = get_logger(__name__)

router = APIRouter(
    tags=["Documents"],
    prefix="/documents",
)


@router.get("/load", status_code=status.HTTP_204_NO_CONTENT)
async def load_documents_route(
    reload: bool = False, product: ProductEnum = ProductEnum.EduTrack
):
    # load environment variables
    load_env()

    # Initialize embedding function and LLM model
    embedding_function = OpenAIEmbeddings()

    # Initialize vector store and load it
    vector_store = VectorStore(embedding_function, os.getenv("VECTOR_STORE_PATH"))

    try:
        logger.info(f"Loading documents for {product.value}")
        documents = load_documents(os.getenv("DOCS_BASE_PATH"), product)
        if reload:
            vector_store.delete_all()

        vector_store.add_documents(documents)
        logger.info(f"Documents {'re' if reload else ''}loaded successfully")
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
