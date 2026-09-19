# Equity Research Agent

A multi-agent LLM pipeline that researches a stock ticker using financial
data (Yahoo Finance), web search (DuckDuckGo via `ddgs`), and FinBERT
sentiment analysis, then produces a structured equity research report
through a LangGraph agent workflow (Fundamental Analyst -> Risk Analyst ->
Debate -> Reflection -> Chief Analyst final report).

## Setup

1. Clone the repo and install dependencies: run `uv sync`
2. Copy `.env.example` to `.env` and add your real OpenAI API key, in the
   form `OPENAI_API_KEY=sk-...`

## Usage

Run `uv run equity-research`

You'll be prompted for a ticker (e.g. AAPL). The pipeline will:
1. Pull financial data and price performance from Yahoo Finance
2. Search the web across several angles (analysis, earnings, risks)
3. Score and filter search results for source quality
4. Run FinBERT sentiment analysis on the filtered results
5. Run a Fundamental Analyst and a Risk Analyst concurrently
6. Debate and reflect on both views
7. Produce a final structured report, saved to a .txt file

## Project structure

- src/equity_research/financial_data.py - Yahoo Finance data fetching
- src/equity_research/web_search.py - DuckDuckGo search + quality scoring
- src/equity_research/sentiment.py - FinBERT sentiment (TextBlob fallback)
- src/equity_research/state.py - Shared LangGraph state schema
- src/equity_research/agents.py - LLM agent node functions
- src/equity_research/pipeline.py - Graph wiring + CLI entry point

## Development

This project was built incrementally using Gitflow - see the commit
history on develop for the full step-by-step evolution from a bare
yfinance script to the current multi-agent pipeline.