import streamlit as st
from pathlib import Path
from langchain.memory import ConversationBufferMemory
import time

folder_files = Path(__file__).parent / "files"
folder_files.mkdir(exist_ok=True) # Garante que a pasta exista

def cria_chain_conversa():
    st.session_state["chain"] = True
    # Mensagens ficticias
    memory = ConversationBufferMemory(return_messages=True)
    memory.chat_memory.add_user_message ("Oi")
    memory.chat_memory.add_ai_message("Olá. Sou PDFBot.")
    st.session_state["memory"] = memory

def chat_app():
    st.header("[robo] Bem vindo ao ChatPDF", divider=True)
    if not "chain" in st.session_state:
        st.error("Faça o upload de pdfs para começar")
        st.stop()

    memory = st.session_state["memory"]
    messages = memory.load_memory_variables({})["history"]
    #st.write(messages)
    container = st.container()
    for message in messages:
        chat = container.chat_message(message.type)
        chat.markdown(message.content)
    
    # simular o envio das mensagens (statico por enquanto)
    new_message = st.chat_input("Converse com os seus documentos")
    if new_message:
        chat = container.chat_message("human")
        chat.markdown(message.content)
        chat = container.chat_message("ai")
        chat.markdown("Gerando Resposta")
        time.sleep(2)
        memory.chat_memory.add_user_message(new_message)
        memory.chat_memory.add_ai_message("Assistente novamente...")
        st.rerun()

def save_uploaded_files(uploaded_files, folder):
    """Salva arquivos enviado na parta especificada."""
    for file in folder.glob("*.pdf"):
        file.unlink()
    # salvar novos arquivo enviados
    for file in uploaded_files:
        (folder / file.name).write_bytes(file.read())

def main():
    with st.sidebar:
        st.header("Upload de PDFs")
        uploaded_pdfs = st.file_uploader("Adicione arquivos PDF",
                                         type="pdf",
                                         accept_multiple_files=True)
        if uploaded_pdfs:
            save_uploaded_files(uploaded_pdfs, folder_files)
            st.success(f"{len(uploaded_pdfs)} arquivo(s) salvo(s) com sucesso!")

        label_botao = "inicializar o chat"
        if "chain" in st.session_state:
            label_botao = "Atualizar chat"
        if st.button(label_botao, use_container_width=True):
            if len(list(folder_files.glob("*.pdf"))) == 0:
                st.error("Adicione arquivos pdf para inicializar o chat")
            else:
                st. success ("Inicializando o Chat...")
                cria_chain_conversa()
                st.rerun()
    
    chat_app()

if __name__ == "__main__":
    main()