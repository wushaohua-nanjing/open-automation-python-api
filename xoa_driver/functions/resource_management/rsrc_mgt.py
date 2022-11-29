from __future__ import annotations

from typing import Any, Dict, List
from xoa_driver.enums import (
    ReservedStatus,
    AutoNegFECOption,
    AutoNegMode,
    AutoNegTecAbility,
    PauseMode,
    LinkTrainingInitCondition,
    LinkTrainingMode,
    NRZPreset,
    PAM4FrameSize,
    TimeoutMode,
)

from xoa_driver.misc import Token
from xoa_driver.utils import apply
from xoa_driver.internals.hli_v2.ports.port_l23.family_l import FamilyL
from xoa_driver.internals.hli_v2.ports.port_l23.family_l1 import FamilyL1
from xoa_driver.ports import GenericAnyPort
from xoa_driver.testers import L23Tester, L47Tester, GenericAnyTester
from xoa_driver.lli import commands

from ..exceptions import (
    NotConnectedError,
    NoSuchModuleError,
)
PcsPmaSupported = (FamilyL, FamilyL1)
AutoNegSupported = (FamilyL, FamilyL1)
LinkTrainingSupported = FamilyL

async def connect(
    tester_type: str,
    host: str,
    username: str,
    password: str = "xena",
    port: int = 22606,
) -> GenericAnyTester:
    """Connect to a Xena tester.

    :param tester_type: Tester type, either "l23" or "l47"
    :type tester_type: str
    :param host: IP address or hostname of the tester.
    :type host: str
    :param username: Username used to log on the tester
    :type username: str
    :param password: Password of the tester, defaults to "xena"
    :type password: str, optional
    :param port: the port number for establishing the TCP connection, defaults to 22606
    :type port: int, optional
    :return: tester object
    :rtype: :class:`~xoa_driver.testers.GenericAnyTester`
    """
    assert tester_type in ("l23", "l47"), "Para 'tester_type' not in ('l23', 'l47')!"
    class_ = {"l23": L23Tester, "l47": L47Tester}[tester_type]
    current_tester = await class_(host, username, password, port, debug=True)
    return current_tester


def get_port(
    tester: GenericAnyTester,
    module_id: int,
    port_id: int,
) -> GenericAnyPort:
    if tester is None:
        raise NotConnectedError()
    try:
        module = tester.modules.obtain(module_id)
    except KeyError:
        raise NoSuchModuleError(module_id)
    try:
        port = module.ports.obtain(port_id)
    except KeyError:
        raise NoSuchModuleError(port_id)
    return port


async def port_reserve(port: GenericAnyPort) -> List[Token]:
    """Reserve a port regardless whether it is owned by others or not.

    :param port: The port to reserve
    :type port: :class:`~xoa_driver.ports.GenericAnyPort`
    :return:
    :rtype: typing.List[Token]
    """
    tokens = []
    r = await port.reservation.get()
    if r.status == ReservedStatus.RESERVED_BY_OTHER:
        tokens.append(port.reservation.set_relinquish())
        tokens.append(port.reservation.set_reserve())
    elif r.status == ReservedStatus.RELEASED:
        tokens.append(port.reservation.set_reserve())
    return tokens


async def port_reset(port: GenericAnyPort) -> List[Token]:
    """Reset a port

    :param port: The port to reset
    :type port: :class:`~xoa_driver.ports.GenericAnyPort`
    :return:
    :rtype: typing.List[Token]
    """
    return [(port.reset.set())]