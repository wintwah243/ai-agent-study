from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq

load_dotenv()

# setup llm
llm = ChatGroq(model="llama-3.3-70b-versatile") 

# response = llm.invoke("What is the capital of France?")
# print(response)