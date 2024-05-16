
############  uses langchain create sql query chain  #################

import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import SQLDatabase
from langchain_cohere import ChatCohere
from langchain_cohere import CohereEmbeddings
from langchain_groq import ChatGroq
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
############ auto execute the query 
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool


groq_api_key = os.getenv("groq_api_key")
llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")

openai_api_key = os.getenv("openai_api_key")
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

db_user = "root"
db_password = "root"
db_host = "localhost"
db_name = "sample"
port = '3306'

db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{port}/{db_name}")

print('#'*100)
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)

##################### creating a final answer chain 

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser() #first chain
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
) #second chain

user_inp = input("enter the question: ")
print(chain.invoke({"question": user_inp}))
