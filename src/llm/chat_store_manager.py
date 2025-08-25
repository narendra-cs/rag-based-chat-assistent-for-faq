from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from src.common.utils import get_logger

logger = get_logger(__name__)


class ChatStoreManager:

    chat_store = {}

    @staticmethod
    def get_chat_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in ChatStoreManager.chat_store:
            ChatStoreManager.chat_store[session_id] = ChatMessageHistory()
            logger.info(f"Chat History for session {session_id} created")
        return ChatStoreManager.chat_store[session_id]

    @staticmethod
    def clear(session_id: str):
        if session_id in ChatStoreManager.chat_store:
            del ChatStoreManager.chat_store[session_id]
            logger.info(f"Chat History for session {session_id} cleared")
        else:
            logger.error(f"Chat History for session {session_id} not found")
