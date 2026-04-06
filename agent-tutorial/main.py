from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import create_react_agent, AgentExecutor 
from tools import search_tool

load_dotenv()

# class which will specify type of content that we want our LLM to return
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    key_findings: list[str]
    sources: list[str]
    tools_used: list[str]
    confidence_score: float
    suggested_next_steps: list[str]


# setup llm
llm = ChatGroq(model="llama-3.3-70b-versatile") 
# response = llm.invoke("What is the capital of France?")
# print(response)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# prompt template setup
prompt = PromptTemplate.from_template("""
You are a research assistant that helps generate structured research responses.

You have access to the following tools:
{tools}

Use this format:

Question: {input}
Thought: think about what to do
Action: one of [{tool_names}]
Action Input: input for the tool
Observation: tool result
... (repeat Thought/Action/Observation if needed)
Thought: I now know the final answer
Final Answer: return the final answer in this format:
{format_instructions}

Question: {input}
Thought: {agent_scratchpad}
""").partial(
    format_instructions=parser.get_format_instructions()
)

# search tool
tools = [search_tool]

# agent setup
agent = create_react_agent(
    llm = llm,
    prompt = prompt,
    tools = tools,  
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research today? ")
raw_response = agent_executor.invoke({"input": query})
# print(raw_response)

try:
    structured_response = parser.parse(raw_response.get("output"))
    print(structured_response)
except Exception as e:
    print("Error parsing response:", e, "\nRaw response was: ", raw_response)


