
from typing import TypedDict


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