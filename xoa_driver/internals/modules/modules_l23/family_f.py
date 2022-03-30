import typing
from xoa_driver import ports
from xoa_driver.internals.utils import ports_manager as pm

if typing.TYPE_CHECKING:
    from xoa_driver.internals.core import interfaces as itf
    from .. import __interfaces as m_itf

from .module_l23_base import ModuleL23

@typing.final
class MOdin10G1S2P(ModuleL23):
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.POdin10G1S2P] = pm.PortsManager(
            conn=conn, 
            ports_type=ports.POdin10G1S2P, 
            module_id=self.module_id,
            ports_count=self.ports_count
        )

@typing.final
class MOdin10G1S2P_b(ModuleL23):
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.POdin10G1S2P_b] = pm.PortsManager(
            conn=conn, 
            ports_type=ports.POdin10G1S2P_b, 
            module_id=self.module_id,
            ports_count=self.ports_count
        )

@typing.final
class MOdin10G1S2P_c(ModuleL23):
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.POdin10G1S2P_c] = pm.PortsManager(
            conn=conn, 
            ports_type=ports.POdin10G1S2P_c, 
            module_id=self.module_id,
            ports_count=self.ports_count
        )

@typing.final
class MOdin10G1S6P(ModuleL23):
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.POdin10G1S6P] = pm.PortsManager(
            conn=conn, 
            ports_type=ports.POdin10G1S6P, 
            module_id=self.module_id,
            ports_count=self.ports_count
        )

@typing.final
class MOdin10G1S6P_b(ModuleL23):
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.POdin10G1S6P_b] = pm.PortsManager(
            conn=conn, 
            ports_type=ports.POdin10G1S6P_b, 
            module_id=self.module_id,
            ports_count=self.ports_count
        )

@typing.final
class MOdin10G1S2PT(ModuleL23):
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.POdin10G1S2PT] = pm.PortsManager(
            conn=conn, 
            ports_type=ports.POdin10G1S2PT, 
            module_id=self.module_id,
            ports_count=self.ports_count
        )

@typing.final
class MOdin10G1S2P_d(ModuleL23):
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.POdin10G1S2P_d] = pm.PortsManager(
            conn=conn, 
            ports_type=ports.POdin10G1S2P_d, 
            module_id=self.module_id,
            ports_count=self.ports_count
        )

@typing.final
class MOdin10G1S12P(ModuleL23):
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.POdin10G1S12P] = pm.PortsManager(
            conn=conn, 
            ports_type=ports.POdin10G1S12P, 
            module_id=self.module_id,
            ports_count=self.ports_count
        )