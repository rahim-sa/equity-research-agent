# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage

# load_dotenv()

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# response = llm.invoke([HumanMessage(content="Say hello in one sentence.")])
# print(response.content)

from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, END

load_dotenv()


class ResearchState(TypedDict):
    ticker: str
    message: str


def data_node(state: ResearchState):
    return {"message": f"Received ticker: {state['ticker']}"}


workflow = StateGraph(ResearchState)
workflow.add_node("data", data_node)
workflow.set_entry_point("data")
workflow.add_edge("data", END)

app = workflow.compile()

if __name__ == "__main__":
    result = app.invoke({"ticker": "AAPL", "message": ""})
    print(result)