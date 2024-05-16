from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_community.document_loaders import (
    WebBaseLoader, TextLoader, PyPDFLoader, youtube, DirectoryLoader
)
from langchain_community.document_loaders import YoutubeLoader
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()


inference_api_key = os.getenv('INFERENCE_API_KEY')
openai_api_key = os.getenv("openai_api_key")

groq_api_key = os.getenv('GROQ_API_KEY')
similarities_top_k = 10

# llm = ChatGroq(temperature=0.0, model_name="llama3-8b-8192")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# embeddings = CohereEmbeddings()
embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=inference_api_key,model_name='sentence-transformers/all-MiniLM-l6-v2')



class Citation(BaseModel):
    source: str = Field(
        description="source in the metadata of the document object."
    )
    page_content: str = Field(
        description="page_content in the document object.",
    )


class CitedAnswer(BaseModel):

    answer: str = Field(
        description="The answer to the user question, which is based only on the given sources.",
    )
    citations: List[Citation] = Field(
        description="All the Document objects referred to answer the user's query.",
    )


def loading_youtube(link):
    loader = YoutubeLoader.from_youtube_url(
    link, add_video_info=False
    )
    text = loader.load()  
    return text

def loading_website(link):
    loader = WebBaseLoader(link)
    docs = loader.load()
    return docs

def loading_pdf(pdf):
    loader = PyPDFLoader(pdf)
    pages = loader.load_and_split()
    return pages

def set_directory_loader( directory_path):    
    loader = DirectoryLoader(
                path=directory_path,
                show_progress=True
            )
    docs = loader.load()
    return docs
            

########## splitting and storing the embeddings ###########

def splitting_storing(text):    
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(text)
    vector = FAISS.from_documents(documents, embeddings)
    return vector


def prompting():
    prompt = ChatPromptTemplate.from_template("""Rules:
    Answer queries only from the given Documents.
    If any query is asked outside Documents say "I don't know".

    Documents:
    {documents}

    User Query:
    {input}""")
    return prompt



llm_model_with_tool = llm.bind_tools(
            tools=[CitedAnswer],
            tool_choice="CitedAnswer"
        )

output_parser = JsonOutputKeyToolsParser(
            key_name="CitedAnswer", first_tool_only=True
        )


