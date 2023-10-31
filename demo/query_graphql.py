import json
import os

import requests
from dotenv import load_dotenv
from rich import print as rprint

load_dotenv()

NETBOX_FQDN = os.getenv("NETBOX_FQDN")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")

GRAPHQL_QUERY = """
query DeviceQuery($deviceName: [String]!) {
    device_list(name: $deviceName) {
        name
        custom_fields
        device_type {
            model
            slug
        }
        platform {
            name
        }
        interfaces {
            name
            ip_addresses {
                address
            }
        }
    }
}
"""

# fmt: off
headers = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

graphql_variables = {"deviceName": "leaf1"}

result = requests.post(
    url=f"{NETBOX_FQDN}/graphql/",
    json={
        "query": GRAPHQL_QUERY,
        "variables": json.dumps(graphql_variables)},
    headers=headers,
).json()
# fmt: on

rprint(result["data"]["device_list"][0])
