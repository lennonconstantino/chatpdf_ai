import streamlit as st
import time
from backend import cria_chain_conversa, folder_files

# folder_files = Path(__file__).parent / "files"
# folder_files.mkdir(exist_ok=True) # Garante que a pasta exista

def chat_app():
    st.header("[robo] Bem vindo ao ChatPDF", divider=True)
    if not "chain" in st.session_state:
        st.error("Faça o upload de pdfs para começar")
        st.stop()

    chain = st.session_state["chain"]
    memory = chain.memory
    messages = memory.load_memory_variables({})["chat_history"]

    container = st.container()
    for message in messages:
        chat = container.chat_message(message.type)
        chat.markdown(message.content)
    
    # simular o envio das mensagens (statico por enquanto)
    new_message = st.chat_input("Converse com os seus documentos")
    if new_message:
        chat = container.chat_message("human")
        chat.markdown(new_message)
        chat = container.chat_message("ai")
        chat.markdown("Gerando Resposta")
        chain.invoke({"question": new_message})
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
