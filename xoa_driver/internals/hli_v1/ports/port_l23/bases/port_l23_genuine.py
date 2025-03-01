import functools
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from xoa_driver.internals.core import interfaces as itf
from xoa_driver.internals.core.commands import (
    P_FLASH,
    P_SPEEDSELECTION,
    P_SPEEDS_SUPPORTED,
    P_UAT_MODE,
    P_UAT_FLR,
    P_STATUS,
    P_TCVRSTATUS,
    P_LOADMODE,
    PP_FECMODE,
)
from xoa_driver.internals.utils import attributes as utils
from xoa_driver.internals.utils.indices import index_manager as idx_mgr
from xoa_driver.internals.hli_v1.indices.streams.genuine_stream import GenuineStreamIdx
from xoa_driver.internals.hli_v1.indices.filter.genuine_filter import GenuineFilterIdx
from xoa_driver.internals.hli_v1.indices.port_dataset import PortDatasetIdx
from xoa_driver.internals.state_storage import ports_state

from .port_l23 import (
    BasePortL23,
    Speed,
    # TxConfiguration,
)

from .port_transceiver import PortTransceiver
from .port_reception_statistics import GenuinePortReceptionStatistics
from .port_transmission_statistics import PortTransmissionStatistics

StreamIndices = idx_mgr.IndexManager[GenuineStreamIdx]
FilterIndices = idx_mgr.IndexManager[GenuineFilterIdx]
PortDatasetIndices = idx_mgr.IndexManager[PortDatasetIdx]


class SpeedMode:
    """L23 port's speed mode"""

    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        self.selection = P_SPEEDSELECTION(conn, module_id, port_id)
        """L23 port speed mode selection.
        
        :type: P_SPEEDSELECTION
        """

        self.supported = P_SPEEDS_SUPPORTED(conn, module_id, port_id)
        """L23 port's supported speed modes.
        
        :type: P_SPEEDS_SUPPORTED
        """


class GenuineSpeed(Speed):
    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        super().__init__(conn, module_id, port_id)
        self.mode = SpeedMode(conn, module_id, port_id)
        """L23 port's speed mode."""


class UnAvailableTime:
    """UnAvailable Time"""

    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        self.mode = P_UAT_MODE(conn, module_id, port_id)
        """L23 port's Unavailable Time mode.
        
        :type: P_UAT_MODE
        """

        self.frame_loss_ratio = P_UAT_FLR(conn, module_id, port_id)
        """L23 port's Frame Loss Ratio for UAT.
        
        :type: P_UAT_FLR
        """


class PortStatistics:
    """L23 port statistics"""

    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        self.rx = GenuinePortReceptionStatistics(conn, module_id, port_id)
        """L23 port's RX statistics."""

        self.tx = PortTransmissionStatistics(conn, module_id, port_id)
        """L23 port's TX statistics."""


class BasePortL23Genuine(BasePortL23):
    """L23 port basic configuration."""

    def __init__(self, conn: "itf.IConnection", module_id: int, port_id: int) -> None:
        super().__init__(conn, module_id, port_id)

        self._local_states = ports_state.PortL23GenuineLocalState()

        self.flash = P_FLASH(conn, module_id, port_id)
        """L23 port flashes.
        
        :type: P_FLASH
        """

        self.status = P_STATUS(conn, module_id, port_id)
        """L23 port's received optical signal level'.
        
        :type: P_STATUS
        """

        self.config_load_mode = P_LOADMODE(conn, module_id, port_id)
        """Chimera Port loading mode.
        
        :type: P_LOADMODE
        """

        self.tcvr_status = P_TCVRSTATUS(conn, module_id, port_id)
        """L23 port transceiver status information.
        
        :type: P_TCVRSTATUS
        """

        self.fec_mode = PP_FECMODE(conn, module_id, port_id)
        """L23 port FEC mode.
        
        :type: PP_FECMODE
        """

        self.speed = GenuineSpeed(conn, module_id, port_id)
        """L23 port speed configuration.

        :type: GenuineSpeed
        """

        self.uat = UnAvailableTime(conn, module_id, port_id)
        """L23 port UnAvailable Time configuration.

        :type: UnAvailableTime
        """

        self.transceiver = PortTransceiver(conn, module_id, port_id)
        """L23 port transceiver configuration.

        :type: PortTransceiver
        """

        self.statistics = PortStatistics(conn, module_id, port_id)
        """L23 port statistics.

        :type: PortStatistics
        """

        self.streams: StreamIndices = idx_mgr.IndexManager(
            conn,
            GenuineStreamIdx,
            module_id,
            port_id
        )
        """L23 port stream index manager.

        :type: StreamIndices
        """

        self.filters: FilterIndices = idx_mgr.IndexManager(
            conn,
            GenuineFilterIdx,
            module_id,
            port_id
        )
        """L23 port filter index manager.

        :type: FilterIndices
        """

        self.datasets: PortDatasetIndices = idx_mgr.IndexManager(
            conn,
            PortDatasetIdx,
            module_id,
            port_id
        )
        """L23 port histogram index manager.

        :type: PortDatasetIndices
        """

    @property
    def info(self) -> ports_state.PortL23GenuineLocalState:
        return self._local_states

    async def _setup(self):
        await self._local_states.initiate(self)
        self._local_states.register_subscriptions(self)
        return self

    on_speed_selection_change = functools.partialmethod(utils.on_event, P_SPEEDSELECTION)
    """Register a callback to the event that the port's speed mode changes."""
