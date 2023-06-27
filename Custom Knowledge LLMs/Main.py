import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlui import css, robot_image, you_image
from langchain.llms import HuggingFaceHub


def extract_text_from_pdfs(pdf_files):
    text = ""
    for pdf_file in pdf_files:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def split_text_into_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def create_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store


def create_conversation_chain(vector_store):
    chat_model = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=chat_model,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_user_question(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(you_image.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(robot_image.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Your personalised PDF assistant", page_icon=":speech_balloon:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Devine Group's LLM")
    user_question = st.text_input("Ask a question:")
    if user_question:
        handle_user_question(user_question)

    with st.sidebar:
        st.subheader("Your PDF Collection")
        pdf_files = st.file_uploader(
            "Upload All PDFs", accept_multiple_files=True)
        if st.button("Run "):
            with st.spinner("run"):
                # Extract text from PDFs
                raw_text = extract_text_from_pdfs(pdf_files)

                # Split text into chunks
                text_chunks = split_text_into_chunks(raw_text)

                # Create vector store
                vector_store = create_vector_store(text_chunks)

                # Create conversation chain
                st.session_state.conversation = create_conversation_chain(vector_store)


if __name__ == '__main__':
    main()
