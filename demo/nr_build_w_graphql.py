#!/usr/bin/env python

import ipaddress
import json
import os

import requests
from config import nr
from dotenv import load_dotenv
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file

load_dotenv()

NETBOX_FQDN = os.getenv("NETBOX_FQDN")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")

J2_FILE = "device.j2"
J2_PATH = "demo/templates"

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


def task_graphql(task: Task, fqdn: str, token: str, query: str) -> Result:
    """
    This task will query NetBox using GraphQL and return the device variables.
    """

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    graphql_variables = {"deviceName": task.host.name}

    result = requests.post(
        url=f"{fqdn}/graphql/",
        json={"query": query, "variables": json.dumps(graphql_variables)},
        headers=headers,
    ).json()

    return Result(host=task.host, result=result["data"]["device_list"][0])


def task_build_config(task: Task, output_path: str) -> Result:
    """
    This task will build the configuration for the device using Jinja2.
    """

    # Collect host variables from NetBox using GraphQL.
    netbox_device_vars = task.run(
        task=task_graphql, fqdn=NETBOX_FQDN, token=NETBOX_TOKEN, query=GRAPHQL_QUERY
    )

    # Render the configuration using Jinja and the variables collected from NetBox.
    rendered_config = task.run(
        task=template_file,
        path=J2_PATH,
        template=J2_FILE,
        ipaddress=ipaddress,
        **netbox_device_vars.result,
    )

    # Write the rendered configuration to a file.
    task.run(
        task=write_file,
        content=rendered_config.result,
        filename=f"{output_path}/{task.host}.txt",
    )

    Result(host=task.host, result=True)


# Run the main build task.
result = nr.run(
    name="Build Configs /w NB + GraphQL",
    output_path="demo/rendered",
    task=task_build_config,
)


# Condition to ensure code below will only be performed when this module is run (i.e not not imported).
if __name__ == "__main__":
    print_result(result)
