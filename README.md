# Automating Config Generation /w NetBox, Nornir and GraphQL

This repo contains the examples and scripts from the Packet Coders webinar:
> Automating Config Generation /w NetBox, Nornir and GraphQL


## Overview
This demo will:
1. Use NetBox as dynamic inventory.
2. Pull down host and interface data from NetBox via GraphQL.
3. Render the a basic device config using Jinja templating and the GraphQL data.
4. Write the rendered configuration to a file.


## Setup

1. Clone repo:
```bash
git clone git@github.com:packetcoders/netbox-nornir-graphql-webinar.git
```

2. Create a `.env`.
```bash
cp .env.example .env
```

3. Populate `.env` with NetBox FQDN and API token.
4. Create virtual environment.
```bash
python -m venv .venv
source .venv/bin/activate
```

5. Install dependancies
```shell
python -m pip install -r requirements.txt
```

## Run the Demo

```bash
./demo/nr_build_w_graphql.py
# Output:
# ./demo/nr_build_w_graphql.py
# Build Configs /w NB + GraphQL**************************************************
# *
# * leaf1 ** changed : False *************************************************
# ****
# vvvv Build Configs /w NB + GraphQL ** changed : False vvvvvvvvvvvvvvvvvvvvvv
# vvvv INFO
# ---- task_graphql ** changed : False ---------------------------------------
# ---- INFO
# { 'custom_fields': { 'domain_name': 'packetcoders.lab',
#                      'ospf_area': '0',
#                      'router_id': '1.1.1.1'},
#   'device_type': {'model': 'Cisco IOSv', 'slug': 'cisco-iosv'},
#   'interfaces': [ { 'ip_addresses': [{'address': '10.1.1
# .2/30'}],
#                     'name': 'GigabitEthernet0/0'},
#                   { 'ip_addresses': [{'address': '10.2.1.2/30'}],
#                     'name': 'GigabitEthernet0/1'},
#                   { 'ip_addresses': [{'address': '172.29.151.103/24'}]
# ,
#                     'name': 'GigabitEthernet0/2'},
#                   {'ip_addresses': [], 'name': 'GigabitEthernet0/3'},
#                   {'ip_addresses': [], 'name': 'GigabitEthernet0/4'},
#                   {'ip_addresses': [], 'name': 'GigabitEthernet0/5'},
#                   {'ip_addresses': [], 'name': 'GigabitEthernet0/6'},
#                   {'ip_addresses': [], 'name': 'GigabitEthernet0/7'},
#                   {'ip_addresses': [], 'name': 'GigabitEthernet0/8'},
#                   {'ip_addresses': [], 'name': 'GigabitEthernet0/9'},
#                   { 'ip_addresses': [{'address': '1.1.1.1/32'}],
#                     'name': 'Loopback 0'}],
...
```

The rendered files can then be located within the rendered directory:

```bash
head -n 20 demo/rendered/leaf1.txt
# Output:
# service timestamps debug datetime msec
# service timestamps log datetime msec
# no service password-encryption
#
# hostname leaf1
#
# boot-start-marker
# boot-end-marker
#
# aaa new-model
# aaa authentication login default local
# aaa session-id common
#
# ip cef
# no ipv6 cef
#
# multilink bundle-name authenticated
#
# interface GigabitEthernet0/0
#   ip address 10.1.1.2 255.255.255.252
```
