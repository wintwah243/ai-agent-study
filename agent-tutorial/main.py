from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

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
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools to gather information.
            Wrap the output in this format and provide on other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# agent setup

