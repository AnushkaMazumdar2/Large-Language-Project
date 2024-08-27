import streamlit as st
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os
from langchain.chains.combine_documents import create_stuff_documents_chain

# Set environment variables
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')

# Initialize Pinecone vector store and LangChain components
index_name = "langchain1"
vector = PineconeVectorStore(index_name=index_name, OllamaEmbeddings(model='mxbai-embed-large'))
groqllm = ChatGroq(model="llama3-70b-8192", temperature=0)

# Define the prompt for the model
prompt = ChatPromptTemplate.from_template("""
Answer the questions based only on the provided context.
Give a precise answer.
<context>
{context}
</context>
Question:{input}
""")

# Create documents chain and retrieval chain
docs = create_stuff_documents_chain(groqllm, prompt)
retrieval = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retrieval, docs)

# Streamlit app
st.title("Library Chatbot")

# User input
user_query = st.text_input("Ask a question about the library:")

if user_query:
    with st.spinner("Searching for an answer..."):
        # Perform a query
        try:
            response = retrieval_chain.invoke({'input': user_query})
            answer = response['answer']
        except Exception as e:
            answer = f"Error: {e}"

    # Display the response
    st.write("**Answer:**")
    st.write(answer)
