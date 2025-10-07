from pydantic import BaseModel, Field, field_validator
import time

class HeaderModel(BaseModel):
    cookie: str = Field(None, alias="Cookie")
    token: str = Field(None, alias="Csrf-Token")

    @field_validator("cookie", mode="before")
    def add_cookie_prefix(cls, value):
        if value and not value.startswith("TPOMADA_SESSIONID="):
            return f"TPOMADA_SESSIONID={value}"
        return value

    class Config:
        populate_by_name = True


class ComplexResponse(BaseModel):
    errorCode: int | None = Field(None)
    msg: str | None = Field(None)
    result: dict | list


class PrivilegeModel(BaseModel):
    sites: list[str]
    all: bool


class UserModel(BaseModel):
    id: str
    role_id: str = Field(None, alias="roleId")
    role_name: str = Field(None, alias="roleName")
    name: str
    email: str
    omada_id: str = Field(None, alias="omadacId")
    privilege: PrivilegeModel
    root: bool


class WanPortModel(BaseModel):
    port_uuid: str = Field(None, alias="portUuid")
    port_name: str = Field(None, alias="portName")
    port_desc: str = Field(None, alias="portDesc")
    wan_port_ipv4_setting: dict = Field(None, alias="wanPortIpv4Setting")


class WlanModel(BaseModel):
    id: str
    name: str
    site: str
    guest: bool = Field(None, alias="guestNetEnable")
    psk_setting: dict = Field(None, alias="pskSetting")
    vlan_id: int = Field(None, alias="vlanId")


class DeviceModel(BaseModel):
    type: str
    mac: str
    name: str
    model: str
    hw_version: str = Field(None, alias="modelVersion")
    fw_version: str = Field(None, alias="firmwareVersion")
    ip: str | None
    uptime: str | None = None
    uptime_long: int = Field(None, alias="uptimeLong")
    status: int
    last_seen: int = Field(None, alias="lastSeen")
    need_upgrade: bool = Field(None, alias="needUpgrade")
    fw_download: bool = Field(None, alias="fwDownload")
    cpu_util: int = Field(None, alias="cpuUtil")
    mem_util: int = Field(None, alias="memUtil")
    download: int | None = None
    upload: int | None = None
    site: str | None
    client_num: int = Field(None, alias="clientNum")
    sn: str | None
    category: str | None = None
    poe_remain: float = Field(None, alias="poeRemain")
    fan_status: int = Field(None, alias="fanStatus")
    poe_support: bool = Field(None, alias="poeSupport")


class ClientModel(BaseModel):
    mac: str
    name: str
    host_name: str = Field(None, alias="hostName")
    device_type: str = Field(None, alias="deviceType")
    ip: str
    connect_type: int = Field(None, alias="connectType")
    connect_dev_type: str = Field(None, alias="connectDevType")
    connected_to_wireless_router: bool = Field(None, alias="connectedToWirelessRouter")
    wireless: bool
    switch_mac: str = Field(None, alias="switchMac")
    switch_name: str = Field(None, alias="switchName")
    stackable_switch: bool = Field(None, alias="stackableSwitch")
    vid: int
    network_name: str = Field(None, alias="networkName")
    dot1x_vlan: int = Field(None, alias="dot1xVlan")
    activity: int
    traffic_down: int = Field(None, alias="trafficDown")
    traffic_up: int = Field(None, alias="trafficUp")
    uptime: int
    last_seen: int = Field(None, alias="lastSeen")
    auth_status: int = Field(None, alias="authStatus")
    guest: bool
    active: bool
    manager: bool
    ip_setting: dict = Field(None, alias="ipSetting")
    down_packet: int = Field(None, alias="downPacket")
    up_packet: int = Field(None, alias="upPacket")
    rate_limit: dict = Field(None, alias="rateLimit")
    standard_port: str = Field(None, alias="standardPort")
    system_name: str | None = Field(None, alias="systemName")
    connect_dev_subtype: int = Field(None, alias="connectDevSubtype")


class GroupMemberIpv4Model(BaseModel):
    ip: str
    mask: int = Field(32)
    description: str = Field("")
    key: int = Field(int(time.time())*1000)

class GroupMemberIpv6Model(BaseModel):
    ip: str
    prefix: int
    key: int = Field(int(time.time())*1000)

class GroupModel(BaseModel):
    group_id: str = Field("", alias="groupId")
    site: str = Field("")
    build_in: bool = Field(False, alias="buildIn")
    name: str
    ip_list: list[GroupMemberIpv4Model] = Field([], alias="ipList")
    ip_v6_list: list[GroupMemberIpv6Model] = Field([], alias="ipv6List")
    count: int
    type: int
    resource: int
    domain_name_port: list = Field(None, alias="domainNamePort")
    port_mask_list: list = Field(None, alias="portMaskList")
    port_type: int = Field(None, alias="portType")
    country_list: list = Field(None, alias="countryList")
    port_list: list = Field(None, alias="portList")
    mac_address_list: list = Field(None, alias="macAddressList")