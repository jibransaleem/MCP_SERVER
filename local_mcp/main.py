import random
from fastmcp import FastMCP
import os
from pathlib import Path
mcp  = FastMCP(name="Demo Server")

@mcp.tool
def roll_dice(n:int ):
    """This method takes a number n and rolls the dice n times  """
    return [random.randint(1,7)for i in range(n)]
    
@mcp.tool
def check_file(name:str):
    """This methods takes file name and checks wheather it exists in cwd or not """
    path =Path(os.getcwd()) / name
    if os.path.exists(str(path)):
        return True
    return False


@mcp.tool
def list_files():
    """ This methods returns the all files located in current working directory"""
    
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    return files
if __name__ == "__main__":
    mcp.run()
    