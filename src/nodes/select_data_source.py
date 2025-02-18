from langchain_core.prompts import ChatPromptTemplate

from configs.prompts import SOURCE_ROUTING_PROMPT

from .base_node import BaseNode

from ..modules.graph_state import GraphState
from ..modules.response_schema import RouteQuery


class SelectDataNode(BaseNode):
    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        chat_llm = self.context.llm
        question = state["question"]

        structured_llm = chat_llm.with_structured_output(RouteQuery)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SOURCE_ROUTING_PROMPT),
                ("human", "{question}"),
            ]
        )

        # Define router
        router = prompt | structured_llm

        response = router.invoke(question)
        print(response.datasource)
        return GraphState(data_source=response.datasource)
