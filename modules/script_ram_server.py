# This function returns a Python object / data type for arguments that specify types used in other languages and frameworks.

from typing import Any

def py_type_for_module_type(t: str) -> str:
    return {
        "decimal": "float",
        "string": "str",
        "integer": "int",
        "boolean": "bool",
    }.get(t.lower(), t.lower())

# This function, given an endpoint, returns a tool name

def tool_name_from_endpoint(endpoint: str) -> str:
    parts = endpoint.rstrip("/").split("/")
    for part in reversed(parts):
        if part and part not in {"steps", "score", "execute"}:
            return part
    return "generated_tool"

# Build starter commands for a RAM FastMCP server

def build_ram_fastmcp_header() -> str:
    lines = ["import os",
             "import requests",
             "import json",
             "from sasram.mcp import tool",
             " ", 
             " "]
    return "\n".join(lines)

# Given a module specification, this tool builds a FastMCP server definition for RAM


def build_ram_fastmcp_tool_def(spec: dict) -> str:
    from urllib.parse import urlsplit
    endpoint = spec["module_endpoint"]
    inputs = spec.get("module_inputs", [])
    outputs = spec.get("module_outputs", [])

    tool_name = tool_name_from_endpoint(endpoint)
    tool_name = tool_name.replace("%", "_").replace("-","_")
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
        "@tool",
        f"def {tool_name}({sig}) -> dict:",
        f'    """Auto-generated tool for {tool_name}."""',
        '    try:',
        f'        input_payload = {{"inputs":[{",".join(payload_items)}]}}',
        f'        url = f\"{{os.getenv(\'VIYA_URL\')}}{server_path}\"',
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

    
def script_mcp_ram_server(filename:str, module_contracts=[]) -> str:
    import os
    with open(os.path.join(filename),"w") as f:
        f.write(build_ram_fastmcp_header())
        for module in module_contracts:
            f.write(build_ram_fastmcp_tool_def(module))
    return f"MCP Server created at {filename}"
