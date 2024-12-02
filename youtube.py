
from utils import llm, embeddings, loading_youtube, loading_website, loading_pdf, splitting_storing, prompting, similarities_top_k, llm_model_with_tool, output_parser


def load_text_from_youtube(youtube_link):

    text = loading_youtube(youtube_link)
    return text

def get_prompt_embedding(human_prompt):

    return embeddings.embed_query(human_prompt)

def find_top_k_similar_documents(vector, prompt_embedding):

    return vector.similarity_search_by_vector(embedding=prompt_embedding, k=similarities_top_k)

def generate_response(prompt, llm_model_with_tool, output_parser, documents, input_text):

    chain = prompt | llm_model_with_tool | output_parser
    return chain.invoke({"documents": documents, "input": input_text})


def main():

    youtube_link = input("Enter the YouTube link: ")
    text = load_text_from_youtube(youtube_link)
    vector = splitting_storing(text)

    human_prompt = input("Enter your query: ")
    prompt_embedding = get_prompt_embedding(human_prompt)

    top_k_similar_documents = find_top_k_similar_documents(vector, prompt_embedding)

    response = generate_response(prompting(), llm_model_with_tool, output_parser, top_k_similar_documents, human_prompt)

    print("Answer:", response["answer"])
    print("Sources:", response["citations"])

if __name__ == "__main__":
    main()
