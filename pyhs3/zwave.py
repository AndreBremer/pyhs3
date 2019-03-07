"""Models Z-Wave devices."""

from .const import (
    DEVICE_ZWAVE_BATTERY,
    DEVICE_ZWAVE_CENTRAL_SCENE,
    DEVICE_ZWAVE_DOOR_LOCK,
    DEVICE_ZWAVE_SENSOR_BINARY,
    DEVICE_ZWAVE_SWITCH_MULTILEVEL,
    DEVICE_ZWAVE_SWITCH,
    DEVICE_ZWAVE_SWITCH_BINARY,
    DEVICE_ZWAVE_BARRIER_OPERATOR,
)
from .device import HomeSeerDevice

STATE_OPENING = "opening"
STATE_CLOSING = "closing"
STATE_OPEN = "open"
STATE_CLOSED = "closed"


class ZWaveBarrierOperator(HomeSeerDevice):
    @property
    def current_state(self):
        if self.value == 0:
            return STATE_CLOSED
        elif self.value == 252:
            return STATE_CLOSING
        elif self.value == 254:
            return STATE_OPENING
        else:
            return STATE_OPEN

    async def open(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._on_value,
        }

        await self._request("get", params=params)

    async def close(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._off_value,
        }

        await self._request("get", params=params)


class ZWaveBattery(HomeSeerDevice):

    pass


class ZWaveCentralScene(HomeSeerDevice):

    pass


class ZwaveDoorLock(HomeSeerDevice):
    @property
    def is_locked(self):
        return self.value == self._lock_value

    async def lock(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._lock_value,
        }

        await self._request("get", params=params)

    async def unlock(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._unlock_value,
        }

        await self._request("get", params=params)


class ZWaveSensorBinary(HomeSeerDevice):

    pass


class ZWaveSwitch(HomeSeerDevice):
    @property
    def is_on(self):
        return self.value > self._off_value

    async def on(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._on_value,
        }

        await self._request("get", params=params)

    async def off(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._off_value,
        }

        await self._request("get", params=params)


class ZWaveSwitchMultilevel(ZWaveSwitch):
    @property
    def dim_percent(self):
        return self.value / self._on_value

    async def dim(self, percent: int):
        value = int(self._on_value * (percent / 100))

        params = {"request": "controldevicebyvalue", "ref": self.ref, "value": value}

        await self._request("get", params=params)


def get_zwave_device(raw, control_data, request):
    device_type = raw["device_type_string"]
    if device_type == DEVICE_ZWAVE_BARRIER_OPERATOR:
        return ZWaveBarrierOperator(raw, control_data, request)
    elif device_type == DEVICE_ZWAVE_BATTERY:
        return ZWaveBattery(raw, control_data, request)
    elif device_type == DEVICE_ZWAVE_CENTRAL_SCENE:
        return ZWaveCentralScene(raw, control_data, request)
    elif device_type == DEVICE_ZWAVE_DOOR_LOCK:
        return ZwaveDoorLock(raw, control_data, request)
    elif device_type == DEVICE_ZWAVE_SENSOR_BINARY:
        return ZWaveSensorBinary(raw, control_data, request)
    elif device_type == DEVICE_ZWAVE_SWITCH:
        return ZWaveSwitch(raw, control_data, request)
    elif device_type == DEVICE_ZWAVE_SWITCH_BINARY:
        return ZWaveSwitch(raw, control_data, request)
    elif device_type == DEVICE_ZWAVE_SWITCH_MULTILEVEL:
        return ZWaveSwitchMultilevel(raw, control_data, request)
