

# steps - 
# 1 import all the libraries and functinons 
# 2 get the api key 
# 3 load the llm models then then embedding model 
# 4 load the doc or the yt 
# 5 store it in a variable 
# 6 splitting the text
# 7 converting into embedding 
# 8 storing the embeddings
# 9 prompting 
# 10 creating the chain 
# 11 retrieve the doc 
# 12 and query the doc 
# 13 get the response 

# youtube 
# pdf
# web 

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
import getpass
import os


os.environ["OPENAI_API_KEY"] = getpass.getpass()
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
embeddings = OpenAIEmbeddings()



#### loaders  ##############

def loading_youtube():
    loader = YoutubeLoader.from_youtube_url(
    "https://youtu.be/0CmtDk-joT4?si=CfrwcHEDcpyQ7ak2", add_video_info=False
    )
    text = loader.load()  
    return text



def loading_website():
    loader = WebBaseLoader("https://www.aryanjangid.com/")
    docs = loader.load()
    return docs

def loading_pdf():
    loader = PyPDFLoader("indraneel_offer.pdf")
    pages = loader.load_and_split()
    return pages

########## splitting and storing the embeddings ###########

def splitting_storing(text):    
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(text)
    vector = FAISS.from_documents(documents, embeddings)
    return vector

######## prompt template #############

def prompting():
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
    <context>
    {context}
    </context>
    Question: {input}""")
    return prompt








