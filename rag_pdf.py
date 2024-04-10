
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
import pdfplumber
import re
import numpy as np

#created the new branch




def extract_text_from_pdf(pdf_path):
    text_list = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_list.append(page.extract_text())
    return text_list


def create_chunks(string, chunk_size = 1000, overlap = 200):
    chunks  = []
    start_index = 0
    end_index = chunk_size

    while start_index < len(string):
        chunk = string[start_index:end_index]
        chunks.append(chunk)
        start_index += chunk_size - overlap
        end_index = min(start_index + chunk_size, len(string))
    
    return chunks

pdf_path = 'pdf_for_rag.pdf'
text_list = extract_text_from_pdf(pdf_path)

print(text_list)
full_text = "\n\n".join(text_list)
chunked_text = create_chunks(full_text)

print(chunked_text)

print(type(chunked_text))
print(len(chunked_text))



# text_chunks = [
#         "Chunk 2: Consectetur adipiscing elit",

#     "I am 22 years old",

#     "Chunk 3: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
# ]

def get_embedding(text, model="text-embedding-ada-002"):
    return client.embeddings.create(model=model, input=[text]).data[0].embedding



embed_arr = []


for text in chunked_text:
    embedding3 = get_embedding(text,model='text-embedding-ada-002')

    embed_arr.append(embedding3)
    # array containing embeddings of chunks


# embedding1 = get_embedding("what is your age?", model='text-embedding-ada-002')


user_prompt= "what is black mountain school?"

User_prompt_embed = get_embedding(user_prompt, model='text-embedding-ada-002')




User_prompt_embed_np = np.array(User_prompt_embed)

similarity = cosine_similarity(embed_arr, [User_prompt_embed_np])

print(similarity)
print(type(similarity))

# similarity.sort()

print(similarity)
most_similar_idx = np.argmax(similarity)

# print(user_prompt)
# print(text_chunks[most_similar_idx])

context = chunked_text[most_similar_idx]
print(context)

# i will be passing the text chunk to the gpt 
# and get the output 


user_query = "what is black mountain school?"

messages =[

    {
        "role":"system",
        "content":f"this is the context {context} use this to answer the query of the user "
    },
    {
        "role":"user",
        "content":f"this is the user query {user_query} you have to use the context provided {context} give the correct output of the query. If you don't know the answer return 'i don't know'"
    }


]

response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Choose the appropriate model
        messages=messages
    )
print("\n\n\n")
print(user_query)
print(response.choices[0].message.content)

