import streamlit as st
from main_rag import responder

st.title("Assistente de Cartões")

if "msgs" not in st.session_state:
    st.session_state.msgs = []

for m in st.session_state.msgs:
    st.chat_message(m["role"]).write(m["content"])

if pergunta := st.chat_input("Digite sua pergunta"):
    st.session_state.msgs.append({"role": "user", "content": pergunta})
    st.chat_message("user").write(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando os documentos..."):
            resposta = responder(pergunta)
        st.write(resposta)

    st.session_state.msgs.append({"role": "assistant", "content": resposta})