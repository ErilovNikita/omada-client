import pytest
import requests
from omada_client import OmadaClient
from .test_data import (
    USER_DATA_CASES, ROUTE_DATA_CASES,
    MAC_DATA_CASES, CLIENT_CASES, WAN_PORT_CASES
)

@pytest.fixture
def client(monkeypatch):
    """Creating a test client instance without a real connection"""
    def fake_auth(self, login, password, site=None):
        self.session = requests.Session()
        self.session_id = "fake_session_id"
        self.csrf = "fake_token"
        self.user_id = "fake_user_id"
        self.sites = ["site"]
        self.site = "site"

    monkeypatch.setattr(OmadaClient, "_OmadaClient__auth", fake_auth)
    return OmadaClient("https://fake.omada.local", "admin", "password")

@pytest.mark.parametrize(
    "login,password,expected_user_id,expected_csrf,expected_session_id",
    USER_DATA_CASES,
    ids=[f"Auth with {case[0]} credentials" for case in USER_DATA_CASES]
)
def test_auth_sets_required_fields(monkeypatch, login, password, expected_user_id, expected_csrf, expected_session_id):
    def fake_get_user_data(self):
        class Dummy:
            omada_id = "u123"
        return Dummy()
    
    monkeypatch.setattr(OmadaClient, "_OmadaClient__get_user_data", fake_get_user_data)
    client = OmadaClient.__new__(OmadaClient)
    client.host = "https://fake.omada.local"

    def fake_login(self, login, password):
        self.csrf = "csrf"
        self.session_id = "id"
        self.user_id = "u123"

    monkeypatch.setattr(OmadaClient, "_OmadaClient__auth", fake_login)
    OmadaClient._OmadaClient__auth(client, login, password)

    assert client.csrf == expected_csrf
    assert client.session_id == expected_session_id
    assert client.user_id == expected_user_id

@pytest.mark.parametrize(
    "mac,expected",
    MAC_DATA_CASES,
    ids=[f"Valid MAC {case[0]} -> {case[1]}" for case in MAC_DATA_CASES]
)
def test_format_mac_address_valid(client, mac, expected):
    assert client._OmadaClient__format_mac_address(mac) == expected

def test_format_mac_address_invalid(client):
    with pytest.raises(ValueError):
        client._OmadaClient__format_mac_address("AA:BB:CC")

@pytest.mark.parametrize(
    "client_data", 
    CLIENT_CASES, 
    ids=[f"Client: {case['name']}" for case in CLIENT_CASES]
)
def test_get_all_clients(client, requests_mock, client_data):
    requests_mock.get(
        f"https://fake.omada.local/{client.user_id}/api/v2/sites/{client.site}/clients", 
        json={"result": {"data": [client_data]}}
    )
    result = client.get_clients()

    assert isinstance(result, list)
    assert result[0].mac == client_data["mac"]
    assert result[0].name == client_data["name"]
    assert result[0].uptime == client_data["uptime"]

@pytest.mark.parametrize(
    "wan_ports", 
    WAN_PORT_CASES, 
    ids=[f"WAN ports: {', '.join([wan['portName'] for wan in case])}" for case in WAN_PORT_CASES]
)
def test_get_all_wan_ports(client, requests_mock, wan_ports):
    requests_mock.get(f"https://fake.omada.local/{client.user_id}/api/v2/sites/{client.site}/setting/wan/networks", json={"result": {"wanPortSettings": wan_ports}})
    result = client.get_all_wan_ports()

    assert isinstance(result, list)
    assert len(result) == len(wan_ports)
    for idx, port in enumerate(wan_ports):
        assert result[idx].port_name == port["portName"]

@pytest.mark.parametrize(
    "client_data", 
    CLIENT_CASES, 
    ids=[f"Client: {case['mac']}" for case in CLIENT_CASES]
)
def test_set_client_fixed_address_success(client, requests_mock, monkeypatch, client_data):
    fake_client_obj = type("FakeClient", (), client_data)()
    monkeypatch.setattr(OmadaClient, "get_client_by_mac", lambda *_: fake_client_obj)

    called = {}

    patch_url = f"https://fake.omada.local/{client.user_id}/api/v2/sites/{client.site}/clients/{fake_client_obj.mac}"
    def track_patch(request, context):
        called["body"] = request.json()
        return {"result": "ok"}

    requests_mock.patch(patch_url, json=track_patch)
    client.set_client_fixed_address_by_mac(fake_client_obj.mac)

    assert "ipSetting" in called["body"]
    assert called["body"]["ipSetting"]["useFixedAddr"] is True
    assert called["body"]["ipSetting"]["ip"] == client_data["ip"]

@pytest.mark.parametrize(
    "route_data", 
    ROUTE_DATA_CASES, 
    ids=[f"Create static route {case[0]}" for case in ROUTE_DATA_CASES]
)
def test_create_static_route(client, requests_mock, route_data):
    requests_mock.post(
        f"https://fake.omada.local/{client.user_id}/api/v2/sites/{client.site}/setting/transmission/staticRoutings", 
        status_code=200, json={"result": "ok"}
    )

    client.create_static_route(
        route_name=route_data[0],
        destinations=route_data[1],
        interface_id=route_data[2],
        next_hop_ip=route_data[3]
    )

    assert requests_mock.called
    assert requests_mock.last_request.json()["name"] == route_data[0]

@pytest.mark.parametrize(
    "case", 
    CLIENT_CASES, 
    ids=[f"Get {case['ip']} by {case['mac']}" for case in CLIENT_CASES]
)
def test_get_client_by_mac_success(client, monkeypatch, case):
    def fake_send_get_request(self, path):
        class R:
            result = case
        return R()
    
    monkeypatch.setattr(OmadaClient, "_OmadaClient__send_get_request", fake_send_get_request)
    result = client.get_client_by_mac(case["mac"])

    assert result.ip == case["ip"]

def test_set_client_fixed_address_not_found(client, monkeypatch):
    def fake_get_client_by_mac(self, mac):
        return None

    monkeypatch.setattr(OmadaClient, "get_client_by_mac", fake_get_client_by_mac)

    with pytest.raises(ValueError, match="Not found device"):
        client.set_client_fixed_address_by_mac("AA:BB:CC:DD:EE:FF")

def test_create_static_route_to_inteface_with_big_data(client, monkeypatch):
    called = []

    def fake_create_static_route(self, *args, **kwargs):
        called.append(kwargs.get("route_name", "unnamed"))

    monkeypatch.setattr(OmadaClient, "create_static_route", fake_create_static_route)

    data = [{
        "name": "routeX",
        "ips": ", ".join([f"10.0.0.{i}" for i in range(40)])
    }]

    client.create_static_route_to_inteface_with_big_data(
        data_static_routes=data,
        interface_id="wan1",
        next_hop_ip="10.0.0.1"
    )

    assert len(called) > 1