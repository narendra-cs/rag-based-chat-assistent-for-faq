from typing import List
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


class ChatInput(BaseModel):
    """ChatInput class to store chatbot input details"""

    query: str = Field(description="Query")
    session_id: str = Field(description="Session ID")

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "What is EduTrack used for?",
                "session_id": "123",
            }
        }
    }


class ChatResponse(BaseModel):
    """ChatResponse class to store chatbot response details"""

    input: str = Field(description="Input")
    answer: str = Field(description="Answer to the query")
    chat_history: List[BaseMessage] = Field(description="Chat history", default=[])
    session_id: str = Field(description="Session ID")

    model_config = {
        "json_schema_extra": {
            "example": {
                "input": "What is EduTrack used for?",
                "answer": "EduTrack is a platform for teachers to create and manage their classes.",
                "chat_history": [
                    {
                        "role": "user",
                        "content": "What is EduTrack used for?",
                    }
                ],
                "session_id": "123",
            }
        }
    }
