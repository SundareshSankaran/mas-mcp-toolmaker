def get_module_urls(modules, viya_host = "") -> list:
    module_urls = []
    for module in modules.get("items", []):
        for link in module.get("links",[]):
            if link["rel"]=="steps":
                module_url = f"{viya_host}{link["uri"]}"
        if "execute" in module["stepIds"]:
            module_url = f"{module_url}/execute"
        elif "score" in module["stepIds"]:
            module_url = f"{module_url}/score"
        else:
            module_url = f"DO NOT USE: {module_url}/score or /execute method not available"
        module_urls.append(module_url)
    return module_urls

def get_module_contracts(module_endpoints: list) -> list:
    import os
    import requests
    access_token = os.getenv("VIYA_ACCESS_TOKEN")
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    module_contracts = []
    for module in module_endpoints:
        if "DO NOT USE: " not in module:
            resp = requests.get(module, headers=headers)
            if resp.status_code==200:
                resp_json = resp.json()
                if "inputs" in resp_json:
                    inputs=resp_json["inputs"]
                else:
                    inputs = [{"message":"No inputs required"}]
                if "outputs" in resp_json:
                    outputs = resp_json["outputs"]
                else:
                    outputs = [{"message":"No outputs"}]
                module_contract = {"module_endpoint": module, "module_inputs": inputs, "module_outputs": outputs} 
                del(inputs)
                del(outputs)
                module_contracts.append(module_contract)
    return module_contracts