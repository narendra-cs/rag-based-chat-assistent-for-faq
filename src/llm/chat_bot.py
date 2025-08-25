from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_core.runnables import RunnableWithMessageHistory, Runnable

from src.llm.chat_store_manager import ChatStoreManager


class ChatBot:

    def __init__(
        self,
        llm,
        retriever,
        enable_history: bool = True,
        query_reformulator_system_prompt: str | None = None,
        answer_synthesizer_prompt: str | None = None,
    ):
        self.llm = llm
        self.retriever = retriever
        self.enable_history = enable_history
        self.query_reformulator_system_prompt = query_reformulator_system_prompt
        self.answer_synthesizer_prompt = answer_synthesizer_prompt
        self.__get_q_and_a_chain()

    def __get_query_reformulator_prompt(self) -> ChatPromptTemplate:
        query_reformulator_system_prompt = self.query_reformulator_system_prompt or (
            """
        You are an expert AI assistant specializing in query reformulation. Your primary task is to rewrite a user's
        latest question to be a self-contained, standalone question by incorporating relevant context from the provided chat history.
        
        However, if the user's question is on a completely new topic and is not a follow-up, you must return the question exactly as it is.

        Use the chat history to understand the conversation and follow-up question.

        <Rules>
        Your rules are:
        1. Analyze the context: Carefully review the chat history to understand the topics, entities (people, places, concepts), and details that have been discussed.
        2. Identify the user's intent: Examine the current question to determine if it's a follow-up question.
            a. A follow-up question often uses pronouns (like "it," "they," "that"), makes comparisons, or asks for more detail about the last-discussed topic.
            b. A new question introduces a topic or entity not present in the recent chat history.
        3. Perform the action:
            a. IF it is a follow-up question:
                i. Rewrite the current question into a clear, specific, and standalone question.
                ii. Replace pronouns (e.g., "it") with the specific nouns they refer to from the chat history (e.g., "the Eiffel Tower").
                iii. Integrate key context to make the question understandable without reading the prior conversation.
                iv. Your output MUST ONLY be the reformulated question text. Do not add any conversational text like "Here is the reformulated question:".
            b. IF it is a new question:
                i. Return the current question verbatim.
                ii. Your output MUST ONLY be the original question text.
        </Rules>
        """
        )

        query_reformulator_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", query_reformulator_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "Question: {input}"),
            ]
        )

        return query_reformulator_prompt

    def __get_answer_synthesizer_prompt(self) -> ChatPromptTemplate:

        answer_system_prompt = self.answer_synthesizer_prompt or (
            """
        You are a helpful Q&A assistant. Your task is to answer the user's query based ONLY on the provided CONTEXT.

        <Rules>
        Your rules are:
        1.  Base your answers strictly on the information given in the CONTEXT.
        2.  Do not use any external knowledge or make assumptions.
        3.  If the answer is not found in the CONTEXT, state clearly that the information is not available in the provided text.
        4.  If you are not sure about the answer, just say "I don't know".
        5.  Do not generate any content that is not directly related to the context.
        6.  keep the answer short and concise.
        </Rules> 
        
        <Context>
        {context}
        </Context>
        """
        )

        answer_prompt = ChatPromptTemplate.from_messages(
            [("system", answer_system_prompt), ("user", "Query: {input}")]
        )

        if self.enable_history:
            answer_prompt.append(MessagesPlaceholder(variable_name="chat_history"))

        return answer_prompt

    def __get_q_and_a_chain(self) -> Runnable:

        retriever = self.retriever
        if self.enable_history:
            query_reformulator_prompt = self.__get_query_reformulator_prompt()
            retriever = create_history_aware_retriever(
                self.llm, retriever, query_reformulator_prompt
            )

        answer_prompt = self.__get_answer_synthesizer_prompt()

        document_chain = create_stuff_documents_chain(
            llm=self.llm, prompt=answer_prompt
        )

        self.q_and_a_chain = create_retrieval_chain(
            retriever=retriever,
            combine_docs_chain=document_chain,
        )

        if self.enable_history:
            self.q_and_a_chain = RunnableWithMessageHistory(
                self.q_and_a_chain,
                ChatStoreManager.get_chat_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer",
                confugration_key="configurable",
            )

        return self.q_and_a_chain

    def chat(self, query: str, session_id: str | None = None) -> Dict[str, Any]:

        if self.enable_history:
            if not session_id:
                raise ValueError("session_id is required when history is enabled")
            config = {"configurable": {"session_id": session_id}}
            return self.q_and_a_chain.invoke({"input": query}, config)
        else:
            return self.q_and_a_chain.invoke({"input": query})
