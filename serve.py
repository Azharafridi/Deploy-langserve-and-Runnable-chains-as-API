from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model= "Gemma2-9b-It", groq_api_key= groq_api_key)

# 1. create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    SystemMessage(content =  system_template),
    HumanMessage(content =  '{text}')
])

parser = StrOutputParser()

## creat chain

chain= prompt_template | model | parser

## App definition
app = FastAPI(title="langchain server",
              version= "1.0",
              description="A simple Langchain server using langchain runnable interfaces"

              )

## Adding chain routes
add_routes(
    app,
    chain,
    path = "/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)