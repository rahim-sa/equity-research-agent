from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

response = llm.invoke([HumanMessage(content="Say hello in one sentence.")])
print(response.content)