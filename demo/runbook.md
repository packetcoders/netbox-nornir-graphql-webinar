## NetBox
- Tenants
- Regions
- Devices
- IP and Interface data
- Custom fields
- All data can be pulled via REST or GraphQL

## GraphQL

### Query 1
```
query {
    device_list {
      name
    }
  }
```

### Query 2
Add further nested objects and fields/attributes
```
query {
  device_list {
    name
    platform {
      name
    }
  }
}

```

### Query 3
Remove query and add filter
```
{
  device_list(name: "leaf1") {
    name
    platform {
      name
    }
  }
}
```

### Query 3
Create a custom query so we can pass in a variable.
```
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

{
  "deviceName": "spine1"
}
```


## Nornir
```
./demo/nr_build_w_graphql.py
```