from fastmcp import FastMCP

mcp = FastMCP("RemoteCalculator")


@mcp.tool
def calculate(a: float, b: float, operation: str) -> float:
    """Perform a calculation using two numbers and an operation."""

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    else:
        raise ValueError(
            "Invalid operation. Use: add, subtract, multiply, or divide"
        )


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )