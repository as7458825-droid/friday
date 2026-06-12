import os


def create_mcp(name: str, tools_csv: str) -> str:
    [t.strip() for t in tools_csv.split(",") if t.strip()]
    code = """from mcp.server import Server
server = Server("{name}")

@server.list_tools()
async def list_tools():
    return [{", ".join(f'Tool(name="{t}", description="{t} tool")' for t in tools)}]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    return {{"result": f"{{name}} called with {{arguments}}"}}
"""
    path = os.path.join(
        os.path.dirname(__file__), "..", "mcp_servers", f"{name}_server.py"
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(code)
    return f"MCP server '{name}' created at {path}"


def add_tool(server_path: str, tool_name: str) -> str:
    if not os.path.isfile(server_path):
        return "Server file not found."
    with open(server_path) as f:
        content = f.read()
    content = content.replace(
        "return [", 'return [Tool(name="{tool_name}", description="{tool_name} tool"), '
    )
    with open(server_path, "w") as f:
        f.write(content)
    return f"Tool '{tool_name}' added."


def test_server(server_path: str) -> str:
    try:
        import ast

        with open(server_path) as f:
            ast.parse(f.read())
        return f"Syntax OK: {server_path}"
    except SyntaxError as e:
        return f"Syntax error: {e}"
