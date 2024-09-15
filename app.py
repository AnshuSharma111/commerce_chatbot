from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from helper import load_document
from helper import split_documents
from helper import addToChroma
from helper import query_rag

CHROMA_PATH = "chroma"
DOC_PATH = 'D:\CodeCubicle3.0\data'

# load document
faq_file = load_document()

# chunk document
chunks = split_documents(faq_file)

# update database
addToChroma(chunks)

# query to the model
while True:
    q = input("Enter your query [Write EXIT to exit]: ")
    if q == "EXIT":
        break
    else:
      query_rag(q)