from dotenv import load_dotenv

load_dotenv()

import os

from langchain_openai import ChatOpenAI, OpenAI


CHATLLM = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

BASELLM = OpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)
