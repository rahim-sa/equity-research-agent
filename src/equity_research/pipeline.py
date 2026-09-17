# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage

# load_dotenv()

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# response = llm.invoke([HumanMessage(content="Say hello in one sentence.")])
# print(response.content)

# from dotenv import load_dotenv
# from typing import TypedDict
# from langgraph.graph import StateGraph, END

# load_dotenv()


# class ResearchState(TypedDict):
#     ticker: str
#     message: str


# def data_node(state: ResearchState):
#     return {"message": f"Received ticker: {state['ticker']}"}


# workflow = StateGraph(ResearchState)
# workflow.add_node("data", data_node)
# workflow.set_entry_point("data")
# workflow.add_edge("data", END)

# app = workflow.compile()

# if __name__ == "__main__":
#     result = app.invoke({"ticker": "AAPL", "message": ""})
#     print(result)

# from dotenv import load_dotenv
# from typing import TypedDict
# from langgraph.graph import StateGraph, END

# from equity_research.financial_data import get_financial_data

# load_dotenv()


# class ResearchState(TypedDict):
#     ticker: str
#     financial_data: str


# def data_node(state: ResearchState):
#     financial = get_financial_data(state["ticker"])
#     return {"financial_data": financial}


# workflow = StateGraph(ResearchState)
# workflow.add_node("data", data_node)
# workflow.set_entry_point("data")
# workflow.add_edge("data", END)

# app = workflow.compile()

# if __name__ == "__main__":
#     result = app.invoke({"ticker": "AAPL", "financial_data": ""})
#     print(result["financial_data"])

from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, END

from equity_research.financial_data import get_financial_data
from equity_research.web_search import web_search
from equity_research.sentiment import summarize_sentiment

load_dotenv()


class ResearchState(TypedDict):
    ticker: str
    financial_data: str
    search_results: list
    sentiment_summary: dict


def data_node(state: ResearchState):
    ticker = state["ticker"]
    financial = get_financial_data(ticker)
    results = web_search(ticker)
    sentiment = summarize_sentiment(results)
    return {
        "financial_data": financial,
        "search_results": results,
        "sentiment_summary": sentiment,
    }


workflow = StateGraph(ResearchState)
workflow.add_node("data", data_node)
workflow.set_entry_point("data")
workflow.add_edge("data", END)

app = workflow.compile()

if __name__ == "__main__":
    result = app.invoke({
        "ticker": "AAPL",
        "financial_data": "",
        "search_results": [],
        "sentiment_summary": {},
    })
    print(result["financial_data"])
    print(result["sentiment_summary"])