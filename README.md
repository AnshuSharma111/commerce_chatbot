# commerce_chatbot
Submission for code cubicle 3.0

This chatbot is a quick and easy way to answer customer regarding Amazon customer support.
This application uses Gemma2 model from Ollama (hosted locally) and answers user queries by querying the model with some context relevant to the question.

The context is obtained by using ChromaDB database where faq.pdf is stored in chunks. For each query, the database provides some context relevant to the query. 
This allows the model to answer the queries concisely and get factual information right.

The tech stack used is:
1) Chroma DB (as a vectorstore)
2) Ollama (for gemma2b)
3) Langchain (for embedding generation)
4) Tkinter (for frontend part of the application)
