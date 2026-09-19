from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


async def fundamental_node(state):
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
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"fundamental_view": response.content}


async def risk_node(state):
    prompt = f"""
You are a skeptical Risk Analyst.
Identify the most material risks facing this company.

Financial Data:
{state['financial_data']}

Web Search Context:
{state['search_context']}

Sentiment Summary:
{state['sentiment_summary']}
"""
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"risk_view": response.content}


async def debate_node(state):
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


async def reflection_node(state):
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


async def final_report_node(state):
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


