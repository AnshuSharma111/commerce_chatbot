from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama


CHROMA_PATH = "chroma"
DOC_PATH = 'D:\CodeCubicle3.0\data'
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def addToChroma(chunks):
  # Load the existing database.
  db = Chroma(
      persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
  )

  # Calculate Page IDs.
  chunks_with_ids = generate_chunk_ids(chunks)

  # Add or Update the documents.
  existing_items = db.get(include=[])  # IDs are always included by default
  existing_ids = set(existing_items["ids"])
  print(f"Number of existing documents in DB: {len(existing_ids)}")

  # Only add documents that don't exist in the DB.
  new_chunks = []
  for chunk in chunks_with_ids:
      if chunk.metadata["id"] not in existing_ids:
          new_chunks.append(chunk)

  if len(new_chunks):
      print(f"👉 Adding new documents: {len(new_chunks)}")
      new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
      db.add_documents(new_chunks, ids=new_chunk_ids)
      db.persist()
  else:
      print("✅ No new documents to add")

def generate_chunk_ids(chunks):
  last_page_id = None
  current_chunk_index = 0

  for chunk in chunks:
      source = chunk.metadata.get("source")
      page = chunk.metadata.get("page")
      current_page_id = f"{source}:{page}"

      # If the page ID is the same as the last one, increment the index.
      if current_page_id == last_page_id:
          current_chunk_index += 1
      else:
          current_chunk_index = 0

      # Calculate the chunk ID.
      chunk_id = f"{current_page_id}:{current_chunk_index}"
      last_page_id = current_page_id

      # Add it to the page meta-data.
      chunk.metadata["id"] = chunk_id

  return chunks

def get_embedding_function():
  embeddings = OllamaEmbeddings(
      model = 'nomic-embed-text'
  )
  return embeddings

def load_document():
  document_loader = PyPDFDirectoryLoader(DOC_PATH)
  return document_loader.load()

def split_documents(documents):
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size = 800,
      chunk_overlap = 80,
      length_function = len,
      is_separator_regex = False,
  )
  return text_splitter.split_documents(documents)


def query_rag(query):
   # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)
    # print(prompt)s

    model = Ollama(model="gemma2")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text