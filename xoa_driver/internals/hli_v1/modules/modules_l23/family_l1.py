import typing
from xoa_driver import ports
from xoa_driver.internals.hli_v1 import revisions
from xoa_driver.internals.utils import ports_manager as pm

if typing.TYPE_CHECKING:
    from xoa_driver.internals.core import interfaces as itf
    from .. import __interfaces as m_itf

from .module_l23_base import ModuleL23
from xoa_driver.internals.core.commands import (
    M_CLOCKPPBSWEEP,
    M_CLOCKSWEEPSTATUS,
)


class MClockSweep:
    """Test module local clock sweep"""
    def __init__(self, conn: "itf.IConnection", module_id: int) -> None:
        self.config = M_CLOCKPPBSWEEP(conn, module_id)
        """Configure and control the module local clock sweep.
        Representation of M_CLOCKPPBSWEEP
        """

        self.status = M_CLOCKSWEEPSTATUS(conn, module_id)
        """Status of the module local clock sweep.
        Representation of M_CLOCKSWEEPSTATUS
        """


class ModuleFamilyL1(ModuleL23):
    """Test module Freya family"""
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)

        self.clock_sweep = MClockSweep(conn, self.module_id)
        """Clock ppm sweep control"""


@typing.final
@revisions.register_valkyrie_module(rev="Freya-800G-1S-1P[a]")
class MFreya800G1S1P_a(ModuleFamilyL1):
    """Test module Freya-800G-1S-1P[a]"""
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.PFreya800G1S1P_a] = pm.PortsManager(
            conn=conn,
            ports_type=ports.PFreya800G1S1P_a,
            module_id=self.module_id,
            ports_count=self.ports_count
        )
        """Port Index Manager of Freya-800G-1S-1P[a]"""


@typing.final
@revisions.register_valkyrie_module(rev="Freya-800G-1S-1P[b]")
class MFreya800G1S1P_b(ModuleFamilyL1):
    """Test module Freya-800G-1S-1P[b]"""
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.PFreya800G1S1P_b] = pm.PortsManager(
            conn=conn,
            ports_type=ports.PFreya800G1S1P_b,
            module_id=self.module_id,
            ports_count=self.ports_count
        )
        """Port Index Manager of Freya-800G-1S-1P[b]"""


@typing.final
@revisions.register_valkyrie_module(rev="Freya-800G-1S-1P-OSFP[a]")
class MFreya800G1S1POSFP_a(ModuleFamilyL1):
    """Test module Freya-800G-1S-1P-OSFP[a]"""
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.PFreya800G1S1POSFP_a] = pm.PortsManager(
            conn=conn,
            ports_type=ports.PFreya800G1S1POSFP_a,
            module_id=self.module_id,
            ports_count=self.ports_count
        )
        """Port Index Manager of Freya-800G-1S-1P-OSFP[a]"""


@typing.final
@revisions.register_valkyrie_module(rev="Freya-800G-4S-1P[a]")
class MFreya800G4S1P_a(ModuleFamilyL1):
    """Test module Freya-800G-4S-1P[a]"""
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.PFreya800G4S1P_a] = pm.PortsManager(
            conn=conn,
            ports_type=ports.PFreya800G4S1P_a,
            module_id=self.module_id,
            ports_count=self.ports_count
        )
        """Port Index Manager of Freya-800G-4S-1P[a]"""


@typing.final
@revisions.register_valkyrie_module(rev="Freya-800G-4S-1P-OSFP[a]")
class MFreya800G4S1POSFP_a(ModuleFamilyL1):
    """Test module Freya-800G-4S-1P-OSFP[a]"""
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.PFreya800G4S1POSFP_a] = pm.PortsManager(
            conn=conn,
            ports_type=ports.PFreya800G4S1POSFP_a,
            module_id=self.module_id,
            ports_count=self.ports_count
        )
        """Port Index Manager of Freya-800G-4S-1P-OSFP[a]"""


@typing.final
@revisions.register_valkyrie_module(rev="Freya-800G-4S-1P[b]")
class MFreya800G4S1P_b(ModuleFamilyL1):
    """Test module Freya-800G-4S-1P[b]"""
    def __init__(self, conn: "itf.IConnection", init_data: "m_itf.ModuleInitData") -> None:
        super().__init__(conn, init_data)
        self.ports: pm.PortsManager[ports.PFreya800G4S1P_b] = pm.PortsManager(
            conn=conn,
            ports_type=ports.PFreya800G4S1P_b,
            module_id=self.module_id,
            ports_count=self.ports_count
        )
        """Port Index Manager of Freya-800G-4S-1P[b]"""
