from __future__ import annotations

from xoa_driver.ports import GenericAnyPort


class ConfigError(Exception):
    msg: str


class NotConnectedError(ConfigError):
    def __init__(self) -> None:
        self.msg = "No tester is connected!"
        super().__init__(self.msg)


class NoSuchModuleError(ConfigError):
    def __init__(self, module_id: int) -> None:
        self.msg = f"No such module {module_id}!"
        super().__init__(self.msg)


class NoSuchPortError(ConfigError):
    def __init__(self, port_id: int) -> None:
        self.msg = f"No such port {port_id}!"
        super().__init__(self.msg)


class NotSupportPcsPmaError(ConfigError):
    def __init__(self, port: GenericAnyPort) -> None:
        module_id, port_id = port.kind.module_id, port.kind.port_id
        self.msg = f"This port {module_id}/{port_id} does not support pcs_pma!"
        super().__init__(self.msg)


class NotSupportAutoNegError(ConfigError):
    def __init__(self, port: GenericAnyPort) -> None:
        module_id, port_id = port.kind.module_id, port.kind.port_id
        self.msg = f"This port {module_id}/{port_id} does not support auto negotiation!"
        super().__init__(self.msg)


class NotSupportLinkTrainError(ConfigError):
    def __init__(self, port: GenericAnyPort) -> None:
        module_id, port_id = port.kind.module_id, port.kind.port_id
        self.msg = f"This port {module_id}/{port_id} does not support link training!"
        super().__init__(self.msg)


class NotRightLaneLengthError(ConfigError):
    def __init__(self, serdes: list[int]) -> None:
        self.msg = f"Serdes {serdes} should be length of 4!"
        super().__init__(self.msg)


class NotRightLaneValueError(ConfigError):
    def __init__(self, serdes: list[int]) -> None:
        self.msg = f"Serdes {serdes} should be a list of 4 integers ranges from 0 to 255!"
        super().__init__(self.msg)



__all__ = (
    "ConfigError",
    "NoSuchModuleError",
    "NoSuchPortError",
    "NotConnectedError",
    "NotRightLaneLengthError",
    "NotRightLaneValueError",
    "NotSupportAutoNegError",
    "NotSupportLinkTrainError",
    "NotSupportPcsPmaError",
)
