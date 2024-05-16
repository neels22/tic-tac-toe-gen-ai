import os
import getpass
from utils import llm, embeddings, loading_youtube, loading_website, loading_pdf, splitting_storing, prompting, similarities_top_k, llm_model_with_tool, output_parser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

def load_text_from_website(website_link):
  
    text = loading_website(website_link)
    return text

def get_prompt_embedding(human_prompt):

    return embeddings.embed_query(human_prompt)

def find_top_k_similar_documents(vector, prompt_embedding):
 
    return vector.similarity_search_by_vector(embedding=prompt_embedding, k=similarities_top_k)

def generate_response(prompt, llm_model_with_tool, output_parser, documents, input_text):

    chain = prompt | llm_model_with_tool | output_parser
    return chain.invoke({"documents": documents, "input": input_text})






def main():

    website_link = input("Enter the website link: ")
    text = load_text_from_website(website_link)
    vector = splitting_storing(text)

    human_prompt = input("Enter your query: ")
    prompt_embedding = get_prompt_embedding(human_prompt)

    top_k_similar_documents = find_top_k_similar_documents(vector, prompt_embedding)

    response = generate_response(prompting(), llm_model_with_tool, output_parser, top_k_similar_documents, human_prompt)

    print("Answer:", response["answer"])
    print("Sources:", response["citations"])

if __name__ == "__main__":
    main()
