from langchain_openai import ChatOpenAI

from sqlite3 import Connection


class Context:
    def __init__(
        self,
        llm: ChatOpenAI,
        llm_stream: ChatOpenAI,
        conn: Connection,
        vs_example,
        vs_data,
    ) -> None:
        self.llm = llm
        self.llm_stream = llm_stream
        self.conn = conn
        self.vs_example = vs_example
        self.vs_data = vs_data
