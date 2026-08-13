from fastmcp import FastMCP
from pathlib import Path


mcp = FastMCP(name="NOTER-TAKER")

BASE_PATH = Path(__file__).resolve().parent
NOTE_DIR = BASE_PATH / "NOTES"

# Create NOTES directory if it doesn't exist
NOTE_DIR.mkdir(exist_ok=True)


def save_to_txt(content, file_name):
    file_path = NOTE_DIR / file_name

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        return f"Successfully written to {file_name}"

    except Exception as e:
        return f"Failed to write {file_name}: {e}"


@mcp.tool()
def save_note(content, task):
    """
    Takes note content and saves it to a file
    using the task as the file name.
    """
    return save_to_txt(content=content, file_name=task)


def retrieve_content(task):
    try:
        file_path = NOTE_DIR / task

        if not file_path.exists():
            return f"{task} does not exist"

        if not file_path.is_file():
            return f"{task} is not a file"

        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        return data

    except Exception as e:
        return f"Failed to retrieve {task}: {e}"


@mcp.tool()
def get_task(task):
    """
    Takes a file name and retrieves its content.
    """
    return retrieve_content(task=task)


@mcp.resource("files://list_files")
def get_all_files():
    """
    Fetches all files in the NOTES directory.
    """
    files = [
        f.name
        for f in NOTE_DIR.iterdir()
        if f.is_file()
    ]

    return files


@mcp.resource("files://{file_name}")
def get_a_file(file_name):
    """
    Checks whether a particular file exists.
    """
    file_path = NOTE_DIR / file_name

    if file_path.is_file():
        return True

    return False


if __name__ == "__main__":
    mcp.run()