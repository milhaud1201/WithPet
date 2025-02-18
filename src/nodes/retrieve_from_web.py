from typing import Dict

import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import SerpAPIWrapper

from configs.default_translate_params import DefaultTranslateParams
from configs.default_web_params import DefaultWebParams

from .base_node import BaseNode

from ..modules.graph_state import GraphState


class WebSearchNode(BaseNode):
    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        chat_llm = self.context.llm
        query = state["question"]

        default_translate_params = DefaultTranslateParams()
        translated = self.ko_to_eng(
            template=default_translate_params.template,
            query=query,
            llm=chat_llm,
        )

        default_web_params = DefaultWebParams()
        output = self.web_search(
            template=default_web_params.template,
            serpapi_params=default_web_params.serpapi_params,
            query=translated,
            llm=chat_llm,
        )
        print(output)
        return GraphState(web_response=output.content)

    def ko_to_eng(
        self,
        template: str,
        query: str,
        llm: ChatOpenAI,
    ) -> str:
        prompt = PromptTemplate(
            template=template,
            input_variables=["query"],
        )

        llm_chain = prompt | llm

        output = llm_chain.invoke(query)
        return output

    def web_search(
        self,
        template: str,
        serpapi_params: Dict[str, str],
        query: str,
        llm: ChatOpenAI,
    ) -> str:

        prompt = PromptTemplate(
            template=template,
            input_variables=["query"],
        )

        llm_chain = prompt | llm

        search = SerpAPIWrapper(
            serpapi_api_key=os.getenv("SERPAPI_API_KEY"),
            params=serpapi_params,
        )

        search_results = search.run(query)
        output = llm_chain.invoke(search_results)
        return output
