def get_initial_count(viya_host ="", access_token="" ) -> int:
    import os
    import requests
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    if viya_host=="":
        viya_host = os.getenv("VIYA_HOST")
        print(f"Viya host URL is {viya_host}")
    if viya_host is None:
        print("Viya URL is not set. Please set the VIYA_HOST environment variable.")
        return 0
    if viya_host:
        if access_token=="":
            access_token = os.getenv("VIYA_ACCESS_TOKEN")
        if access_token is None:
            print("Access token missing. Please set the VIYA_ACCESS_TOKEN environment variable.")
        if access_token:
            response = requests.get(f"{viya_host}/microanalyticscore/modules", headers=headers)
            if response.status_code == 200:
                response_json = response.json()
                return response_json.get("count", 0)
            else:
                print(f"Failed to retrieve modules. Status code: {response.status_code}")
                return 0

def get_all_modules(viya_host="", access_token="", cnt_modules=0 ) -> dict:
    import os
    import requests
    if cnt_modules > 0:
        access_token = os.getenv("VIYA_ACCESS_TOKEN")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        if viya_host=="":
            viya_host = os.getenv("VIYA_HOST")
        if viya_host is None:
            print("Viya host URL is not set. Please set the VIYA_HOST environment variable.")
            return {"error": "Viya URL is not set."}
        if viya_host:
            if access_token=="":
                access_token = os.getenv("VIYA_ACCESS_TOKEN")
            if access_token is None:
                print("Access token missing. Please set the VIYA_ACCESS_TOKEN environment variable.")
            if access_token:
                response = requests.get(f"{viya_host}/microanalyticscore/modules?limit={cnt_modules}", headers=headers)
                if response.status_code == 200:
                    response_json = response.json()
                    return response_json
                else:
                    print(f"Failed to retrieve modules. Status code: {response.status_code}")
                    return {"error": f"Failed to retrieve modules. Status code: {response.status_code}"}
        else:
            print("Viya host URL is not set. Please set the VIYA_HOST environment variable.")
            return {"error": "Viya URL is not set."}