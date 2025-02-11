from configs.default_translate_params import DefaultTranslateParams
from configs.default_web_params import DefaultWebParams

from .base_node import BaseNode

from ..models.graph_state import GraphState
from ..utils.translate import ko_to_eng
from ..utils.web_search import web_search


class WebSearchNode(BaseNode):
    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        chatllm = self.context.llm
        query = state["question"]

        default_translate_params = DefaultTranslateParams()
        translated = ko_to_eng(
            template=default_translate_params.template, query=query, llm=chatllm
        )

        default_web_params = DefaultWebParams()
        output = web_search(
            template=default_web_params.template,
            serpapi_params=default_web_params.serpapi_params,
            query=translated,
            llm=chatllm,
        )
        print(output)
        return GraphState(web_response=output.content)
