import os
from fastapi import APIRouter, HTTPException, status
from langchain_openai.embeddings import OpenAIEmbeddings

from src.common.vector_store import VectorStore
from src.common.utils import get_logger, get_llm, load_env
from src.llm.chat_bot import ChatBot
from src.llm.chat_store_manager import ChatStoreManager
from src.pydentic_models.models import ChatResponse, ChatInput


logger = get_logger(__name__)

router = APIRouter(
    tags=["Chat"],
    prefix="/chat",
)


@router.post("/", status_code=status.HTTP_200_OK, response_model=ChatResponse)
async def chat(chat_input: ChatInput):
    load_env()

    try:
        logger.info(f"Chatting with {chat_input.session_id}")
        # Initialize embedding function and LLM model
        embedding_function = OpenAIEmbeddings()

        # Initialize vector store and load it
        vector_store = VectorStore(embedding_function, os.getenv("VECTOR_STORE_PATH"))
        retriever = vector_store.get_retriever()

        chatbot = ChatBot(
            llm=get_llm(),
            retriever=retriever,
            enable_history=True,
        )
        response = chatbot.chat(
            query=chat_input.query, session_id=chat_input.session_id
        )
        logger.info(f"Query: {chat_input.query}")
        logger.info(f"Response: {response['answer']}")
        return {**response, "session_id": chat_input.session_id}
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(session_id: str):
    try:
        logger.info(f"Deleting chat history for {session_id}")
        ChatStoreManager.clear(session_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
