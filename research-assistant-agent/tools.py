from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from datetime import datetime

# Function to save research output to a .txt file which is necessary for my custom tool
def save_to_txt_file(input_string: str):
    raw_data = str(input_string)
    if ", filename=" in raw_data:
        raw_data = raw_data.split(", filename=")[0]
    
    lines = raw_data.split(". ")
    formatted_data = ".\n\n".join([line.strip() for line in lines if line.strip()])
    if not formatted_data.endswith("."):
        formatted_data += "."

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "research_output.txt"
    
    output_content = (
        f"{'='*30}\n"
        f"RESEARCH OUTPUT ({timestamp})\n"
        f"{'='*30}\n\n"
        f"{formatted_data}\n\n"
    )
    
    with open(filename, "a", encoding="utf-8") as file:
        file.write(output_content)    
    
    return f"Successfully formatted and saved to {filename}"


# custom tool setup for saving research output to a .txt file
save_tool = Tool(
    name="save_text_to_txt_file",
    func=save_to_txt_file,
    description="Save text to a .txt file.",
)

# tools setup that can access search that I will be using in my agent
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search_web",
    func=search.run,
    description="Search the web for recent information.",
)

# wikipedia tool setup
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
