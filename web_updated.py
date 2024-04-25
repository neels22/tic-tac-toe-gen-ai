
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import getpass
import os
from utils import llm,embeddings,loading_youtube,loading_website,loading_pdf,splitting_storing,prompting


llm=llm
embeddings=embeddings

text = loading_website()

try: 
    vector = splitting_storing(text)
except Exception as e:

    print("An error occurred while processing the text:", e)
 
    exit(1)


prompt = prompting()

document_chain = create_stuff_documents_chain(llm, prompt)

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "who is aryan?"})
print(response["answer"])
