import streamlit as st
from conexiones.OpenAIConnection import OpenAIConnection


def main():
    api_key = st.secrets["OPENAI_API_KEY"]
    OpenAI = OpenAIConnection(api_key)

    if prompt := st.chat_input(placeholder="Escribe lo que quieras"):
        with st.chat_message("user"):
            st.write(prompt)
        response = OpenAI.generarPalabraConMemoria(prompt)
        with st.chat_message("assistant"):
            st.write(response.content)


if __name__ == "__main__":
    main()
