from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message
from langchain_core.prompts import PromptTemplate
mcp = FastMCP(name = "my-mcp")

# static resource
@mcp.resource("config://settings")
def get_settings():
    return {
        "version":1.0,
        "updated_date" : "01-01-2019"
    }
    
NOTE = {
    "1" : "apple",
    "2" : "ball"
 }

# dynamic resouce
@mcp.resource("notes://{note_id}")
def get_notes(note_id):
    return NOTE.get(note_id , "NICE TRY DIDY")
HISTORY = []        
@mcp.resource("HISTORY://my_history")
def get_data():
    return HISTORY

@mcp.tool()
def show_data(n:int):
    """This method  a number n and gives its product with 2"""
    res  =n*2
    HISTORY.append(res)
    return res
@mcp.prompt
def summarize_text(topic: str) -> str:
    """Prompt to summarize a given topic"""
    return f"Summarize the content of the topic '{topic}' in a few words."

@mcp.prompt
def prompts_for_image(type:str):
    """ PROMPT TO GENRATE A GOOD IMAGE OF GIVEN TYPE"""
    return [
        Message(role  = "user" , content  = f"Genrate an image of type{type}")
    ]
if __name__ == "__main__":
    mcp.run()