import os
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.common.utils import get_logger, ProductEnum


logger = get_logger(__name__)


def load_documents(docs_base_path: str, product: ProductEnum) -> list[Document]:

    docs_file_path = os.path.join(docs_base_path, product.value)

    if Path(docs_file_path).exists():
        logger.info(f"Loading documents from {docs_file_path}")
        loader = PyPDFDirectoryLoader(docs_file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        return text_splitter.split_documents(documents)
    else:
        logger.error(f"Documents not found at {docs_file_path}")
        raise FileNotFoundError(f"Documents not found at {docs_file_path}")
