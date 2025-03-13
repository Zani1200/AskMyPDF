from typing import List

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


class OpenAIConnection:

    def __init__(self, api_key):
        self.llm = ChatOpenAI(api_key=api_key, temperature=0.7, max_tokens=150)

    def generarPalabraConMemoria(self,prompt):

        promptAI = ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente útil que responde preguntas de manera clara y concisa."),
            ("human", f"{prompt}"),
        ])
        humanMessage = promptAI.messages[1].prompt.template
        systemMessage = promptAI.messages[0].prompt.template
        return self.llm.invoke([systemMessage, humanMessage])


