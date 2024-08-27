from langchain_groq import ChatGroq # Inference Engine
from langchain_community.document_loaders.csv_loader import CSVLoader # For loading CSV
from langchain.text_splitter import RecursiveCharacterTextSplitter # For chunking
from langchain_pinecone import PineconeVectorStore # To store the vector embeddings
from langchain_community.embeddings import OllamaEmbeddings # For vector embeddings
from langchain.chains.combine_documents import create_stuff_documents_chain # Type of chain
from langchain.prompts import ChatPromptTemplate # For prompts
from langchain.chains import create_retrieval_chain # Combining chain and retriever
from langchain.chains.summarize import load_summarize_chain # For summarizing
import os

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')

data = CSVLoader(r"C:\Users\Anushka\OneDrive\Desktop\LLM Project\combined_library_data.csv")

prompt = ChatPromptTemplate.from_template("""
                                          
                                          Answer the questions based only on the provided context.
                                          Give a precise answer.
                                          <context>
                                          {context} 
                                          </context>
                                          Question:{input}
                                          
                                          """)

loader = data.load()

chunks = RecursiveCharacterTextSplitter(chunk_size = 200, chunk_overlap = 0)
split_data = chunks.split_documents(loader)

index_name = "langchain1"
vector = PineconeVectorStore.from_documents(split_data,OllamaEmbeddings(model='mxbai-embed-large'),index_name = index_name)
groqllm = ChatGroq(model="llama3-70b-8192", temperature = 0)
docs = create_stuff_documents_chain(groqllm, prompt)
retrieval = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retrieval,docs)
res = retrieval_chain.invoke({'input': 'How many books are there for Architecture?'})
res['answer']

