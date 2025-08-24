# chatbot.py
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# ===============================
# Load Documents (FAQ + Resume)
# ===============================
def load_documents():
    docs = []

    # Load FAQ (text file)
    try:
        faq_loader = TextLoader("faq.txt")
        docs += faq_loader.load()
    except:
        pass

    # Load Resume (PDF)
    try:
        pdf_loader = PyPDFLoader("resume.pdf")
        docs += pdf_loader.load()
    except:
        pass

    return docs

# ===============================
# Create Vector DB
# ===============================
@st.cache_resource
def create_vector_db():
    docs = load_documents()
    if not docs:
        return None

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs_split = splitter.split_documents(docs)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Store in FAISS
    db = FAISS.from_documents(docs_split, embeddings)
    return db

# ===============================
# Load LLM
# ===============================
@st.cache_resource
def load_llm():
    model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=256)
    return HuggingFacePipeline(pipeline=pipe)

# ===============================
# Chatbot UI
# ===============================
def chatbot():
    st.markdown("<h3 style='text-align: center;'>🤖 Ask Me Anything</h3>", unsafe_allow_html=True)

    # Initialize retriever + QA chain
    db = create_vector_db()
    llm = load_llm()

    if db:
        retriever = db.as_retriever(search_kwargs={"k": 3})
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    else:
        qa_chain = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User input
    query = st.text_input("💬 Your Question:", key="chat_input")

    if st.button("Send"):
        if query:
            if qa_chain:
                try:
                    response = qa_chain.invoke(query)
                    answer = response["result"]
                except Exception as e:
                    answer = f"⚠️ Error generating response: {e}"
            else:
                answer = "⚠️ Knowledge base not loaded. Please upload FAQ/Resume."

            # Save conversation
            st.session_state.chat_history.append(("You", query))
            st.session_state.chat_history.append(("Bot", answer))

    # Display conversation
    for speaker, text in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"<div style='text-align:right;'><b>{speaker}:</b> {text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; color:#34D399;'><b>{speaker}:</b> {text}</div>", unsafe_allow_html=True)
