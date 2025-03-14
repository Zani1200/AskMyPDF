from langchain.indexes import VectorstoreIndexCreator
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS


class OpenAIConnection:

    def __init__(self, api_key, vectorStore):
        self.llm = ChatOpenAI(api_key=api_key, temperature=0.7)
        self.vectorStore = vectorStore

    def lecturaPDF(self,prompt):
        # Configurar la memoria de la conversación
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Esto sirve para que el modelo siga esto pasos, es decir una cadena
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorStore.as_retriever(),
            memory=memory
        )

        return qa_chain.invoke({"question": prompt, "chat_history": memory.buffer})


