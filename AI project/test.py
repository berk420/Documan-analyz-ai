#!/usr/bin/env python
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langserve import add_routes
from transformers import pipeline
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel


dotenv_path = Path('key.env')
load_dotenv(dotenv_path=dotenv_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)


llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=OPENAI_API_KEY)

fill_mask = pipeline(
    "fill-mask",
    model="google/mobilebert-uncased",
    tokenizer="google/mobilebert-uncased"
)

class JokeRequest(BaseModel):
    message: str

class JokeRequest(BaseModel):
    topic: str

@app.post("/test1")
async def test_endpoint(request: JokeRequest):

    user_input = request.message

    result =f"{user_input}{fill_mask.tokenizer.mask_token}"

    response=fill_mask(result)

    return {"message": response}


@app.get("/test")
async def test_endpoint():
    return {"message": "This is a test string!"}


template = PromptTemplate(
        input_variables=["question"],
        template="Bunu bana karadeniz şivesiyle söyle: {question}"
    )


@app.post("/joke")
async def joke_endpoint(request: JokeRequest):
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

    user_input = "tell me a simple joke?"

    formatted_prompt = template.format(question=user_input)

    messages = [{"role": "user", "content": formatted_prompt}]
    response = llm.invoke(messages)
    return {"joke": response}


@app.get("/test")
async def test_endpoint():
    return {"message": "This is a test string!"}

if __name__ == "__main__":
    import uvicorn
    import nest_asyncio
    nest_asyncio.apply()

    uvicorn.run(app, host="localhost", port=8000)