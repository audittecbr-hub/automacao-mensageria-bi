import os
import requests
from dotenv import load_dotenv
load_dotenv()
from src.core.clients.powerbi_client import PowerBIClient

client = PowerBIClient(workspace_id=os.getenv("POWERBI_WORKSPACE_ID"))
client.authenticate()
token = client.token

headers = {"Authorization": f"Bearer {token}"}
url = f"https://api.powerbi.com/v1.0/myorg/groups/{os.getenv('POWERBI_WORKSPACE_ID')}/datasets"
res = requests.get(url, headers=headers)
print("Status:", res.status_code)
if res.status_code == 200:
    datasets = res.json().get("value", [])
    for d in datasets:
        print(f"Dataset: {d.get('name')} | ID: {d.get('id')}")
else:
    print(res.text)
