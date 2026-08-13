from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
import json
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


def load_model():
    model = ChatGroq(
        api_key=os.getenv("GROQ"),
        model="llama-3.1-8b-instant"
    )
    return model


SERVERS = {
    "Demo Server": {
        "transport": "stdio",
        "command": r"C:\Users\ADIL TRADERS\Desktop\MY_MCP_SERVER\.venv\Scripts\python.exe",
        "args": [r"C:\Users\ADIL TRADERS\Desktop\MY_MCP_SERVER\main.py"]
    },
    "deepwiki": {
        "transport": "streamable_http",
        "url": "https://mcp.deepwiki.com/mcp",
    },
}


async def main(prompt):
    client = MultiServerMCPClient(SERVERS)

    tools = await client.get_tools()
    print("Available tools:", [t.name for t in tools])

    tool_dict = {}
    for tool in tools:
        tool_dict[tool.name] = tool

    model = load_model()
    llm_with_tools = model.bind_tools(tools)
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    tool_messages = []
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        result = await tool_dict[selected_tool].ainvoke(selected_tool_args)
        tool_messages.append(
            ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result))
        )

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    print(f"Final response: {final_response.content}")


if __name__ == "__main__":
    asyncio.run(main("List the files in my current direcory? and checks if jibran.py exists in it or not?"))