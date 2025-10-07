USER_DATA_CASES = [
    ("admin", "pass123", "u123", "csrf", "id"),
    ("user", "secret", "u123", "csrf", "id"),
]

ROUTE_DATA_CASES = [
    ("TestRoute1", ["192.168.0.0/24"], "wan1", "192.168.0.1"),
    ("TestRoute2", ["10.0.0.0/16"], "wan2", "10.0.0.1"),
]

MAC_DATA_CASES = [
    ("aabbccddeeff", "AA-BB-CC-DD-EE-FF"),
    ("112233445566", "11-22-33-44-55-66"),
]

CLIENT_CASES = [
    {
        "name": "client_one",
        "wireless": False,
        "vid": 0,
        "activity": 0,
        "uptime": 1000,
        "guest": False,
        "active": True,
        "manager": False,
        "ip": "192.168.1.10",
        "mac": "AA-BB-CC-DD-EE-FF",
        "ip_setting": {"netId": "net100"}
    },
    {
        "name": "client_two",
        "wireless": True,
        "vid": 1,
        "activity": 5,
        "uptime": 500,
        "guest": True,
        "active": False,
        "manager": False,
        "ip": "192.168.1.20",
        "mac": "11-22-33-44-55-66",
        "ip_setting": {"netId": "net200"}
    }
]

WAN_PORT_CASES = [[
    {"portName": "WAN1"}, 
    {"portName": "WAN2"},
]]