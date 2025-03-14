import streamlit as st
import pdfplumber
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from conexiones.OpenAIConnection import OpenAIConnection

def chatBot(api_key, vectorStore):

    if vectorStore is None:
        st.warning("No hay datos de vectorstore disponibles. Asegúrate de cargar un PDF correctamente.")
        return

    OpenAI = OpenAIConnection(api_key, vectorStore)

    # Mostrar los mensajes anteriores
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input(placeholder="Escribe lo que quieras"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        response = OpenAI.lecturaPDF(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
        with st.chat_message("assistant"):
            st.write(response['answer'])


#Esto sirve para que una vez se cargue, si vuelve a ser el mismo PDF no tenga que hacer de nuevo la funcion
@st.cache_data
def mostrarPDF(pdf_upload) -> list:
    pdf_pages = []
    with pdfplumber.open(pdf_upload) as pdf:
        pdf_pages = [page.to_image(resolution=300).original for page in pdf.pages]
        return pdf_pages


def leerPDF(pdf_upload, api_key):
    pdf_upload.seek(0)
    with pdfplumber.open(pdf_upload) as pdf:

        pdf_text = ""
        for page in pdf.pages:
            pdf_text += page.extract_text()

        # 🔹 **Dividir texto en fragmentos para embeddings**
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_text(pdf_text)


        # 🔹 **Convertir texto en embeddings y guardarlos en FAISS**
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_texts(texts, embedding=embeddings)

        # Guardar el vectorstore en la sesión
        st.session_state.vectorstore = vectorstore


def main() -> None:

    st.set_page_config(layout="wide")

    api_key = st.secrets["OPENAI_API_KEY"]

    col1, col2 = st.columns([1.5,2])

    # Inicializamos el session_state de mensajes
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Inicializamos el session_state del vectorStore
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None


    with col1.container(height=800, border=True,):

        pdf_upload = st.file_uploader("Sube un archivo PDF", type="pdf", accept_multiple_files=False)

        if pdf_upload is not None:

            leerPDF(pdf_upload,api_key)

            images = mostrarPDF(pdf_upload)
            for i, img in enumerate(images):
                st.image(img, use_container_width=True)

            st.success("📄 PDF procesado correctamente. ¡Haz preguntas!")

    with col2:
        chatBot(api_key, st.session_state.vectorstore)

if __name__ == "__main__":
    main()
