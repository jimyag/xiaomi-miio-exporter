#!/usr/bin/env python3
from time import sleep, time
from miio import Device
from os.path import isfile
import prometheus_client as pc
import config

# 设置默认端口如果配置文件没有设置
prometheus_port = getattr(config, "prometheus_port", 8000)

pc.start_http_server(prometheus_port)
electric_power_gauge = pc.Gauge(
    name="xiaomi_cuco_plug_v3_electric_power",
    documentation="Power of the device",
    labelnames=["device_ip", "device_name"],
)

max_power_limit_gauge = pc.Gauge(
    name="xiaomi_cuco_plug_v3_max_power_limit",
    documentation="Max power limit of the device",
    labelnames=["device_ip", "device_name"],
)

power_limit_extension_gauge = pc.Gauge(
    name="xiaomi_cuco_plug_v3_power_limit_extension",
    documentation="Power limit extension of the device",
    labelnames=["device_ip", "device_name"],
)

switch_state_gauge = pc.Gauge(
    name="xiaomi_cuco_plug_v3_switch_up",
    documentation="Switch up state of the device (0: off, 1: on)",
    labelnames=["device_ip", "device_name"],
)
switch_fault_state_gauge = pc.Gauge(
    name="xiaomi_cuco_plug_v3_switch_fault",
    documentation="Switch fault state of the device (0: no fault, 1: Over Temperature ,2: Overload)",
    labelnames=["device_ip", "device_name"],
)


# 客厅插座
class CUCOPlugV3(Device):
    def set(self, SIID, PIID, VALUE):
        return self.send(
            "set_properties",
            [{"did": f"set-{SIID}-{PIID}", "piid": PIID, "siid": SIID, "value": VALUE}],
        )

    def get(self, SIID, PIID):
        return self.send(
            "get_properties",
            [{"did": f"set-{SIID}-{PIID}", "piid": PIID, "siid": SIID}],
        )

    def electric(self) -> int:  # 功率
        data = self.get(11, 2)
        if data:
            return data[0]["value"]

    def max_power_limit(self) -> int:  # 最大功率限制
        data = self.get(9, 2)
        if data:
            return data[0]["value"]

    def power_limit_extension(self) -> int:  # 功率限制扩展
        data = self.get(15, 1)
        if data:
            return data[0]["value"]

    def switch_up(self) -> bool:  # 开关状态
        data = self.get(2, 2)
        if data:
            return data[0]["value"]

    def switch_fault(self) -> int:  # 开关故障状态
        data = self.get(2, 3)
        if data:
            return data[0]["value"]


if __name__ == "__main__":
    devices = getattr(config, "devices", [])
    if not devices:
        print("No devices found in config.py")
        exit(1)
    for device in devices:
        print(f"Device: {device['name']} - {device['ip']}")
    while True:
        for device in devices:
            plug = CUCOPlugV3(device["ip"], device["token"])
            electric_power_gauge.labels(
                device_ip=plug.ip, device_name=device["name"]
            ).set(plug.electric())
            max_power_limit_gauge.labels(
                device_ip=plug.ip, device_name=device["name"]
            ).set(plug.max_power_limit())
            power_limit_extension_gauge.labels(
                device_ip=plug.ip, device_name=device["name"]
            ).set(plug.power_limit_extension())
            switch_state_gauge.labels(
                device_ip=plug.ip, device_name=device["name"]
            ).set(plug.switch_up())
            switch_fault_state_gauge.labels(
                device_ip=plug.ip, device_name=device["name"]
            ).set(plug.switch_fault())

        sleep(5)
