import streamlit as st
from conexiones.OpenAIConnection import OpenAIConnection


def main():
    try:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        api_key = st.secrets["OPENAI_API_KEY"]
        OpenAI = OpenAIConnection(api_key)

        # Mostrar los mensajes anteriores
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if prompt := st.chat_input(placeholder="Escribe lo que quieras"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            response = OpenAI.generarPalabraConMemoria(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            with st.chat_message("assistant"):
                st.write(response.content)

    except KeyError:
        st.error("La clave API no está definida en `st.secrets`.")
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
