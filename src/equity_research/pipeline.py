

from equity_research.agents import (
    fundamental_node,
    risk_node,
    debate_node,
    reflection_node,
    final_report_node,
)


from equity_research.state import ResearchState
from equity_research.web_search import web_search, format_search_results
#from equity_research.web_search import web_search
#from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from equity_research.financial_data import get_financial_data

from equity_research.sentiment import summarize_sentiment

from dotenv import load_dotenv


load_dotenv()
import os

if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit(
        "OPENAI_API_KEY is not set. Add it to your .env file before running this script."
    )


def data_node(state: ResearchState):
    ticker = state["ticker"]
    financial = get_financial_data(ticker)
    results = web_search(ticker)
    sentiment = summarize_sentiment(results)
    search_context = format_search_results(results)
    return {
        "financial_data": financial,
        "search_results": results,
        "sentiment_summary": sentiment,
        "search_context": search_context,
    }


workflow = StateGraph(ResearchState)
workflow.add_node("data", data_node)
workflow.add_node("fundamental", fundamental_node)
workflow.add_node("risk", risk_node)
workflow.add_node("debate", debate_node)
workflow.add_node("reflection", reflection_node)
workflow.set_entry_point("data")
workflow.add_edge("data", "fundamental")
workflow.add_edge("data", "risk")
workflow.add_edge("fundamental", "debate")
workflow.add_edge("risk", "debate")
workflow.add_edge("debate", "reflection") # Added
#workflow.add_edge("debate", END)
#workflow.add_edge("reflection", END) # added
#workflow.add_node("reflection", reflection_node)
workflow.add_node("final", final_report_node)
workflow.add_edge("reflection", "final")
workflow.add_edge("final", END)

app = workflow.compile()




async def main():
    from datetime import datetime

    ticker = input("Enter ticker: ").strip().upper()

    result = await app.ainvoke({
        "ticker": ticker,
        "financial_data": "",
        "search_results": [],
        "sentiment_summary": {},
        "search_context": "",
        "fundamental_view": "",
        "risk_view": "",
        "debate": "",
        "reflection": "",
        "final_report": "",
    })

    print(result["final_report"])

    filename = f"{ticker}_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result["final_report"])
    print(f"\nSaved to {filename}")



def cli():
    import asyncio
    asyncio.run(main())


if __name__ == "__main__":
    cli()