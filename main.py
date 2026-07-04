import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun, Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

# 1. Create the Tools
search = DuckDuckGoSearchRun()
def calculate(expression: str) -> str:
    try:
        return str(eval(expression))
    except:
        return "Math Error"
math_tool = Tool(name="Calculator", func=calculate, description="Useful for math")

tools = [search, math_tool]

# 2. Create the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 3. Create the Prompt
prompt = PromptTemplate.from_template("""
You are a helpful assistant. You must use the tools to answer.
Question: {input}
{agent_scratchpad}
""")

# 4. Create the Agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

# 5. Run it
if __name__ == "__main__":
    question = input("Ask a complex question: ")
    try:
        result = agent_executor.invoke({"input": question})
        print("\nFinal Answer:", result['output'])
    except Exception as e:
        print("Error:", e)
