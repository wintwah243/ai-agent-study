from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from datetime import datetime

# tools setup that can access search that we will be using in our agent
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search_web",
    func=search.run,
    description="Search the web for recent information.",
    
)