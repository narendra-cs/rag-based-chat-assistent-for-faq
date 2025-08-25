from langchain.embeddings.base import Embeddings
from langchain.schema import BaseRetriever
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from src.common.utils import get_logger

logger = get_logger(__name__)


class VectorStore:
    _instance: "VectorStore" = None
    _initialized: bool = False
    _vector_store: Chroma | None = None

    def __new__(cls, embedding_function: Embeddings, persist_directory: str = None):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
        return cls._instance

    def __init__(self, embedding_function: Embeddings, persist_directory: str = None):
        if not self._initialized:
            self.embedding_function = embedding_function
            self.persist_directory = persist_directory
            self._vector_store = Chroma(
                collection_name="faq_vector_collection",
                embedding_function=self.embedding_function,
                persist_directory=self.persist_directory,
            )
            self._initialized = True

    @property
    def vector_store(self) -> Chroma:
        if self._vector_store is None:
            raise ValueError("Vector store not initialized")
        return self._vector_store

    def add_documents(self, documents: list[Document]):
        self.vector_store.add_documents(documents)
        logger.info("Documents added to vector store")

    def similarity_search(self, query: str, k: int = 3) -> list[Document]:
        logger.info(f"Similarity search for query: {query}")
        return self.vector_store.similarity_search(query, k=k)

    def delete(self, document_ids: list[str]):
        self.vector_store.delete(ids=document_ids)
        logger.info("Document deleted from vector store")

    def delete_all(self):
        if self.vector_store._collection.count() > 0:
            all_documents = self.vector_store._collection.get()
            all_ids = all_documents["ids"]
            self.vector_store.delete(ids=all_ids)
            logger.info("All documents deleted from vector store")
        else:
            logger.info("No documents in vector store, skipping deletion")

    def persist(self):
        if self._vector_store is not None:
            self._vector_store.persist()
            logger.info("Vector store persisted")

    def get_retriever(
        self, search_type: str = "similarity", k: int = 3, **kwargs
    ) -> BaseRetriever:
        search_kwargs = {"k": k, **kwargs}
        logger.info(
            f"Retrieving documents using {search_type} search type with {search_kwargs}"
        )
        return self.vector_store.as_retriever(
            search_type=search_type, search_kwargs=search_kwargs
        )
