# Import tool_name_from_endpoint function

from .get_module_info import tool_name_from_endpoint

# This function returns a Python object / data type for arguments that specify types used in other languages and frameworks.

from typing import Any

def py_type_for_module_type(t: str) -> str:
    return {
        "decimal": "float",
        "string": "str",
        "integer": "int",
        "boolean": "bool",
    }.get(t.lower(), t.lower())



# Build starter commands for an HTTP FastMCP server

def build_http_fastmcp_header() -> str:
    lines = ["import os",
             "import requests",
             "from fastapi import FastAPI",
             "import uvicorn",
             "from mcp.server.fastmcp import FastMCP",
             "from dotenv import load_dotenv",
             "",
             "load_dotenv()",
             "",
             "mcp = FastMCP(\"generated-http-server\", json_response=True )",
             " ", 
             " "]
    return "\n".join(lines)

# Given a module specification, this tool builds a FastMCP server definition


def build_fastmcp_tool_def(spec: dict) -> str:
    from urllib.parse import urlsplit
    endpoint = spec["module_endpoint"]
    inputs = spec.get("module_inputs", [])
    outputs = spec.get("module_outputs", [])

    tool_name = tool_name_from_endpoint(endpoint)
    tool_name = tool_name.replace("%", "_").replace("-","_")
    if "module_description" in spec:
         if any(char.isalpha() for char in spec["module_description"]):
            tool_description = spec["module_description"]
        else:
            tool_description = f"Auto-generated tool for {tool_name}."
    else:
        tool_description = f"Auto-generated tool for {tool_name}."
    # server_path = endpoint.replace("/steps/score", "/steps/execute")
    server_path = urlsplit(endpoint).path

    params = []
    payload_items = []
    for item in inputs:
        if item!= {'message': 'No inputs required'}:
            name = item["name"]
            if item["name"][0].isdigit() or item["name"][0]=="_":
                param_name = f"p_{item["name"]}"
            else:
                param_name = item["name"]
            param_name = param_name.replace(".","_")
            py_type = py_type_for_module_type(item.get("type", "Any"))
            params.append(f"{param_name}: {py_type}")
            payload_items.append(f'{{"name":"{name}","value":{param_name}}}')

    sig = ", ".join(params)
    output_names = [o["name"] for o in outputs if o!= {'message': 'No outputs'}]

    lines = [
        " ",
        "@mcp.tool()",
        f"def {tool_name}({sig}) -> dict:",
        f'    """{tool_description}"""',
        '    try:',
        f'        input_payload = {{"inputs":[{",".join(payload_items)}]}}',
        f'        url = f\"{{os.getenv(\'VIYA_HOST\')}}{server_path}\"',
        '        access_token = os.getenv("VIYA_ACCESS_TOKEN")',
        '        headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}',
        '        resp = requests.post(url=url, headers=headers, json=input_payload)',
        "        data = resp.json()",
    ]

    if output_names:
        lines.append("        return data")
    else:
        lines.append("        return {'message':'No output expected'}")

    lines.append("    except Exception as e:")
    lines.append("        return {\"error\": str(e)}")
    lines.append(" ")

    return "\n".join(lines)

# Build footer (starting service) commands for an HTTP MCP server

def build_http_fastmcp_server_script() -> str:
    lines = [" ",
             "app = FastAPI()",
             "",
             "",
             "# Mount MCP at /mcp",
             "app.mount(\"/mcp\", mcp.streamable_http_app())",
             "@app.get(\"/\")",
             "def root():",
             "    return {\"status\": \"ok\", \"mcp\": \"/mcp\"}",
             "",
             "if __name__ == \"__main__\":",
             "    uvicorn.run(app, host=\"localhost\", port=8000)",
             " "]
    return "\n".join(lines)
    
def script_mcp_http_server(filename:str, module_contracts=[]) -> str:
    import os
    with open(os.path.join(filename),"w") as f:
        f.write(build_http_fastmcp_header())
        for module in module_contracts:
            f.write(build_fastmcp_tool_def(module))
        f.write(build_http_fastmcp_server_script())
    return f"MCP Server created at {filename}"
