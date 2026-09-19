
from equity_research.web_search import web_search, format_search_results
#from equity_research.web_search import web_search
from typing import TypedDict
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



llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


# class ResearchState(TypedDict):
#     ticker: str
#     financial_data: str
#     search_results: list
#     sentiment_summary: dict
#     fundamental_view: str
#     risk_view: str
#     debate: str
#     reflection: str
#     final_report: str

class ResearchState(TypedDict):
    ticker: str
    financial_data: str
    search_results: list
    sentiment_summary: dict
    search_context: str
    fundamental_view: str
    risk_view: str
    debate: str
    reflection: str
    final_report: str


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


# def fundamental_node(state: ResearchState):
#     prompt = f"""
# You are a senior Fundamental Equity Analyst.
# Analyze this company's business quality, growth, profitability, and valuation.

# Financial Data:
# {state['financial_data']}

# Sentiment Summary:
# {state['sentiment_summary']}
# """
#     response = llm.invoke([HumanMessage(content=prompt)])
#     return {"fundamental_view": response.content}

#def fundamental_node(state: ResearchState):

async def fundamental_node(state: ResearchState):    
    prompt = f"""
You are a senior Fundamental Equity Analyst.
Analyze this company's business quality, growth, profitability, and valuation.

Financial Data:
{state['financial_data']}

Web Search Context:
{state['search_context']}

Sentiment Summary:
{state['sentiment_summary']}
"""
    # response = llm.invoke([HumanMessage(content=prompt)])
    # return {"fundamental_view": response.content}

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"fundamental_view": response.content}

#def risk_node(state: ResearchState):
async def risk_node(state: ResearchState):
    prompt = f"""
You are a skeptical Risk Analyst.
Identify the most material risks facing this company.

Financial Data:
{state['financial_data']}

Sentiment Summary:
{state['sentiment_summary']}

Web Search Context:
{state['search_context']}

"""
    # response = llm.invoke([HumanMessage(content=prompt)])
    # return {"risk_view": response.content}
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"risk_view": response.content}

async def debate_node(state: ResearchState):
    prompt = f"""
Moderate a sharp debate between these two views.
Highlight the strongest points, contradictions, and key tensions.

Fundamental View:
{state['fundamental_view']}

Risk View:
{state['risk_view']}
"""
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"debate": response.content}

async def reflection_node(state: ResearchState):
    prompt = f"""
You are a senior investment professional. Critically evaluate the reasoning
quality and balance of the fundamental and risk views. Give clear guidance
for what the final rating should weigh most heavily.

Fundamental:
{state['fundamental_view']}

Risk:
{state['risk_view']}

Debate:
{state['debate']}
"""
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"reflection": response.content}


async def final_report_node(state: ResearchState):
    prompt = f"""
You are the Chief Equity Analyst. Write a structured final research report.

Structure:
**1. Company Overview**
**2. Fundamental Assessment**
**3. Key Risks**
**4. Market Sentiment**
**5. Key Debate Points**
**6. Investment Thesis** (Bull Case / Bear Case)
**7. Final Rating** (Strongly Bullish / Bullish / Cautiously Bullish / Neutral / Cautiously Bearish / Bearish) with justification

Financial Data:
{state['financial_data']}

Sentiment Summary:
{state['sentiment_summary']}

Fundamental View:
{state['fundamental_view']}

Risk View:
{state['risk_view']}

Debate:
{state['debate']}

Reflection:
{state['reflection']}
"""
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"final_report": response.content} 


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




# if __name__ == "__main__":
#     from datetime import datetime

#     ticker = input("Enter ticker: ").strip().upper()
 
#     result = app.invoke({
#     "ticker": ticker,
#     "financial_data": "",
#     "search_results": [],
#     "sentiment_summary": {},
#     "search_context": "",
#     "fundamental_view": "",
#     "risk_view": "",
#     "debate": "",
#     "reflection": "",
#     "final_report": "",
# })

#     print(result["final_report"])

#     filename = f"{ticker}_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
#     with open(filename, "w", encoding="utf-8") as f:
#         f.write(result["final_report"])
#     print(f"\nSaved to {filename}")


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


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

    