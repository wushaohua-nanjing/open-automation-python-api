"""P4_ 	Port L47"""
from dataclasses import dataclass
import typing
import functools

from ..protocol.command_builders import (
    build_get_request,
    build_set_request
)
from .. import interfaces
from ..transporter.token import Token
from ..protocol.fields.data_types import *
from ..protocol.fields.field import XmpField
from ..registry import register_command
from .enums import *

@register_command
@dataclass
class P4_TRAFFIC:
    """
    Gives a traffic state command to a L47 port.
    """

    code: typing.ClassVar[int] = 700
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class SetDataAttr:
        traffic_state: XmpField[XmpByte] = XmpField(XmpByte, choices=TrafficState)  # coded byte, the traffic state command issued to the port.

    def set(self, traffic_state: TrafficState) -> "Token":
        return Token(self._connection, build_set_request(self, module=self._module, port=self._port, traffic_state=traffic_state))

    set_off = functools.partialmethod(set, TrafficState.OFF)
    set_on = functools.partialmethod(set, TrafficState.ON)
    set_stop = functools.partialmethod(set, TrafficState.STOP)
    set_prepare = functools.partialmethod(set, TrafficState.PREPARE)
    set_prerun = functools.partialmethod(set, TrafficState.PRERUN)


@register_command
@dataclass
class P4_STATE:
    """
    Display the current state of the port.
    """

    code: typing.ClassVar[int] = 701
    pushed: typing.ClassVar[bool] = True

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        state: XmpField[XmpByte] = XmpField(XmpByte, choices=PortState)  # coded byte, specifying the current state for this port.

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_CAPABILITIES:
    """
    Report the speeds supported by the port.
    """

    code: typing.ClassVar[int] = 702
    pushed: typing.ClassVar[bool] = True

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        auto: XmpField[XmpByte] = XmpField(XmpByte)  # byte, autoneg supported
        N100_mbps: XmpField[XmpByte] = XmpField(XmpByte)  # byte, 100M speed supported
        N1_gbps: XmpField[XmpByte] = XmpField(XmpByte)  # byte, 1G speed supported
        N2_5_gbps: XmpField[XmpByte] = XmpField(XmpByte)  # byte, 2.5G speed supported
        N5_gbps: XmpField[XmpByte] = XmpField(XmpByte)  # byte, 5G speed supported
        N10_gbps: XmpField[XmpByte] = XmpField(XmpByte)  # byte, 10G speed supported
        N25_gbps: XmpField[XmpByte] = XmpField(XmpByte)  # byte, 25G speed supported
        N40_gbps: XmpField[XmpByte] = XmpField(XmpByte)  # byte, 40G speed supported
        N50_gbps: XmpField[XmpByte] = XmpField(XmpByte)  # byte, 50G speed supported
        N100_gbps: XmpField[XmpByte] = XmpField(XmpByte)  # byte, 100G speed supported

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_STATE_STATUS:
    """
    Returns status of the last port state change. If the port state has changed to
    PREPARE_FAIL, the status contains information about the reason for the fail.
    Currently the status will be "OK"in all other states.
    """

    code: typing.ClassVar[int] = 703
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        status: XmpField[XmpStr] = XmpField(XmpStr)  # string, status for the last port state change

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_VLAN_OFFLOAD:
    """
    Specifies if 802.1Q VLAN tag should be inserted and stripped by the Ethernet
    device. If VLAN Offload is switched ON, VLAN tags will not be present in frames
    captured by the L47 Server.
    """

    code: typing.ClassVar[int] = 704
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class SetDataAttr:
        offload: XmpField[XmpByte] = XmpField(XmpByte, choices=OnOff)  # coded byte, specifies if VLAN Offload is switched ON

    @dataclass(frozen=True)
    class GetDataAttr:
        offload: XmpField[XmpByte] = XmpField(XmpByte, choices=OnOff)  # coded byte, specifies if VLAN Offload is switched ON

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))

    def set(self, offload: OnOff) -> "Token":
        return Token(self._connection, build_set_request(self, module=self._module, port=self._port, offload=offload))

    set_off = functools.partialmethod(set, OnOff.OFF)
    set_on = functools.partialmethod(set, OnOff.ON)


@register_command
@dataclass
class P4_ARP_CONFIG:
    """
    Configure the value of the arp request transmission rate, retransmission timeout
    and max. retries.
    """

    code: typing.ClassVar[int] = 705
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class SetDataAttr:
        rate: XmpField[XmpInt] = XmpField(XmpInt)  # integer, ARP Request transmission rate (requests / sec) - must be larger than 0
        retrans_timeout: XmpField[XmpInt] = XmpField(XmpInt)  # integer, ARP Request retransmission timeout [ms] - must be larger than 0
        retries: XmpField[XmpByte] = XmpField(XmpByte)  # byte, maximum ARP Request retransmission retries

    @dataclass(frozen=True)
    class GetDataAttr:
        rate: XmpField[XmpInt] = XmpField(XmpInt)  # integer, ARP Request transmission rate (requests / sec) - must be larger than 0
        retrans_timeout: XmpField[XmpInt] = XmpField(XmpInt)  # integer, ARP Request retransmission timeout [ms] - must be larger than 0
        retries: XmpField[XmpByte] = XmpField(XmpByte)  # byte, maximum ARP Request retransmission retries

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))

    def set(self, rate: int, retrans_timeout: int, retries: int) -> "Token":
        return Token(self._connection, build_set_request(self, module=self._module, port=self._port, rate=rate, retrans_timeout=retrans_timeout, retries=retries))


@register_command
@dataclass
class P4_NDP_CONFIG:
    """
    Configure the value of the NDP Neighbor Solicitation transmission rate,
    retransmission timeout and max. retries.
    """

    code: typing.ClassVar[int] = 706
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class SetDataAttr:
        rate: XmpField[XmpInt] = XmpField(XmpInt)  # integer, NDP Neighbor Solicitation transmission rate (requests / sec) - must be larger than 0
        retrans_timeout: XmpField[XmpInt] = XmpField(XmpInt)  # integer, NDP Neighbor Solicitation retransmission timeout [ms] - must be larger than 0
        retries: XmpField[XmpByte] = XmpField(XmpByte)  # byte, Max. NDP Neighbor Solicitation retransmission retries

    @dataclass(frozen=True)
    class GetDataAttr:
        rate: XmpField[XmpInt] = XmpField(XmpInt)  # integer, NDP Neighbor Solicitation transmission rate (requests / sec) - must be larger than 0
        retrans_timeout: XmpField[XmpInt] = XmpField(XmpInt)  # integer, NDP Neighbor Solicitation retransmission timeout [ms] - must be larger than 0
        retries: XmpField[XmpByte] = XmpField(XmpByte)  # byte, Max. NDP Neighbor Solicitation retransmission retries

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))

    def set(self, rate: int, retrans_timeout: int, retries: int) -> "Token":
        return Token(self._connection, build_set_request(self, module=self._module, port=self._port, rate=rate, retrans_timeout=retrans_timeout, retries=retries))


@register_command
@dataclass
class P4_CAPTURE:
    """
    Description Starts and stops packet capture on this port. Parameters
    """

    code: typing.ClassVar[int] = 707
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class SetDataAttr:
        on_off: XmpField[XmpByte] = XmpField(XmpByte, choices=OnOff)  # coded byte, specifying whether to capture traffic on this port

    @dataclass(frozen=True)
    class GetDataAttr:
        on_off: XmpField[XmpByte] = XmpField(XmpByte, choices=OnOff)  # coded byte, specifying whether to capture traffic on this port

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))

    def set(self, on_off: OnOff) -> "Token":
        return Token(self._connection, build_set_request(self, module=self._module, port=self._port, on_off=on_off))

    set_off = functools.partialmethod(set, OnOff.OFF)
    set_on = functools.partialmethod(set, OnOff.ON)


@register_command
@dataclass
class P4_CAPTURE_GET_FIRST:
    """
    Returns the first captured frame on the port. Command is only valid when port is
    in state STOPPED
    """

    code: typing.ClassVar[int] = 708
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        index: XmpField[XmpInt] = XmpField(XmpInt)  # integer, index of frame returned
        second: XmpField[XmpInt] = XmpField(XmpInt)  # integer, second value of frame capture timestamp
        microsecond: XmpField[XmpInt] = XmpField(XmpInt)  # integer, microsecond value of frame capture timestamp
        capture_length: XmpField[XmpInt] = XmpField(XmpInt)  # integer, length of captured portion of the frame
        frame_length: XmpField[XmpInt] = XmpField(XmpInt)  # integer, length of the frame
        frame: XmpField[XmpHexList] = XmpField(XmpHexList)  # list of hex bytes, the captured frame (capture_len bytes)

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_CAPTURE_GET_NEXT:
    """
    Returns the next captured frame on the port. Command is only valid when port is
    in state STOPPED
    """

    code: typing.ClassVar[int] = 709
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        index: XmpField[XmpInt] = XmpField(XmpInt)  # integer, index of frame returned
        second: XmpField[XmpInt] = XmpField(XmpInt)  # integer, second value of frame capture timestamp
        microsecond: XmpField[XmpInt] = XmpField(XmpInt)  # integer, usec value of frame capture timestamp
        capture_length: XmpField[XmpInt] = XmpField(XmpInt)  # integer, length of captured portion of the frame
        frame_length: XmpField[XmpInt] = XmpField(XmpInt)  # integer, length of the frame
        frame: XmpField[XmpHexList] = XmpField(XmpHexList)  # hexdata, the captured frame (capture_len bytes)

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_ETH_TX_COUNTERS:
    """
    Return total port Ethernet transmit statistics since last clear.
    """

    code: typing.ClassVar[int] = 710
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        bits_per_sec: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, bit/second of (layer 2) bytes transmitted
        packets_per_sec: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, packets/second of packets transmitted
        byte_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of (layer 2) bytes transmitted
        packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of packets transmitted

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_ETH_RX_COUNTERS:
    """
    Return total port Ethernet receive statistics since last clear.
    """

    code: typing.ClassVar[int] = 711
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        bits_per_sec: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, bit/second of (layer 2) bytes received
        packets_per_sec: XmpField[XmpLong] = XmpField(XmpLong)  # long, integer packets/second of received packets
        byte_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of (layer 2) bytes received
        packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of packets received

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_PORT_TX_COUNTERS:
    """
    Return total port transmit statistics since last clear.
    """

    code: typing.ClassVar[int] = 712
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        vlan_packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of 802.1Q VLAN tagged packets transmitted
        bits_per_sec: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, bit/second of (layer 1) bits transmitted.
        byte_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of (layer 1) bytes received.

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_PORT_RX_COUNTERS:
    """
    Return total port receive statistics since last clear.
    """

    code: typing.ClassVar[int] = 713
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        vlan_packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of 802.1Q VLAN tagged packets received
        bits_per_sec: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, bit/second of (layer 1) bits received.
        byte_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of (layer 1) bytes received.

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_PORT_COUNTERS:
    """
    Return total port transmit statistics since last clear.
    """

    code: typing.ClassVar[int] = 714
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        invalid_eth_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of invalid (e.g. short) Ethernet packets received
        unknown_eth_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of unknown or unsupported Ethernet packets received
        mismatch_vlan_error_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of packets with mismatching vlan info received
        pkt_rate_limit_count: XmpField[XmpLong] = XmpField(
            XmpLong
        )  # long integer, number of times that number of packets transmitted has been limited by the maximum packet rate limiter.

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_TX_PACKET_SIZE:
    """
    Return histogram over transmitted (layer 2) packets sizes in 100 bytes
    intervals.
    """

    code: typing.ClassVar[int] = 715
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        bin_00: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_01: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_02: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_03: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_04: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_05: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_06: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_07: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_08: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_09: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_10: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_11: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_12: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_13: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_14: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_15: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_RX_PACKET_SIZE:
    """
    Return histogram over received (layer 2) packets sizes in 100 bytes intervals.
    """

    code: typing.ClassVar[int] = 716
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        bin_00: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_01: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_02: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_03: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_04: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_05: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_06: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_07: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_08: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_09: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_10: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_11: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_12: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_13: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_14: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.
        bin_15: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of packets received with a (layer 2) size in the given interval.

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_TX_MTU:
    """
    Return histogram over transmitted (layer 3) packets sizes in 1 byte intervals.
    Each bin represents a packet size in the interval [576..1500] bytes.
    """

    code: typing.ClassVar[int] = 717
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        bins: XmpField[XmpByteList] = XmpField(XmpByteList)  # 925 x byte, '1' if any packets were transmitted with the specified layer 3 size, otherwise '0'.

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_RX_MTU:
    """
    Return histogram over received (layer 3) packets sizes in 1 byte intervals. Each
    bin represents a packet size in the interval [576..1500] bytes.
    """

    code: typing.ClassVar[int] = 718
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        bins: XmpField[XmpByteList] = XmpField(XmpByteList)  # 925 x byte, '1' if any packets were received with the specified layer 3 size, otherwise '0'.

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_IPV4_RX_COUNTERS:
    """
    Return total Port IPv4 protocol receive statistics since last clear.
    """

    code: typing.ClassVar[int] = 719
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of IPv4 packets received

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_IPV4_TX_COUNTERS:
    """
    Return total Port IPv4 protocol transmit statistics since last clear.
    """

    code: typing.ClassVar[int] = 720
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of IPv4 packets transmitted

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_IPV4_COUNTERS:
    """
    Return total Port IPv4 protocol statistics since last clear.
    """

    code: typing.ClassVar[int] = 721
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        checksum_error_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of IPv4 packets which ip header checksum error
        invalid_packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of IPv4 packets which are malformed
        unknown_packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of IPv4 packets with unknown protocol

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_IPV6_RX_COUNTERS:
    """
    Return total Port IPv6 protocol receive statistics since last clear.
    """

    code: typing.ClassVar[int] = 722
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of IPv6 packets received

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_IPV6_TX_COUNTERS:
    """
    Return total Port IPv6 protocol transmit statistics since last clear.
    """

    code: typing.ClassVar[int] = 723
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of IPv6 packets transmitted

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_IPV6_COUNTERS:
    """
    Return total Port IPv6 protocol statistics since last clear.
    """

    code: typing.ClassVar[int] = 724
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        invalid_packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ipv6 packets which are malformed
        unknown_packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ipv6 packets with unknown protocol

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_ARP_RX_COUNTERS:
    """
    Return total Port ARP protocol receive statistics since last clear.
    """

    code: typing.ClassVar[int] = 725
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        arp_request_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number ARP Requests received
        arp_reply_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number ARP Replies received

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_ARP_TX_COUNTERS:
    """
    Return total Port ARP protocol transmit statistics since last clear.
    """

    code: typing.ClassVar[int] = 726
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        arp_request_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number ARP Requests transmitted
        arp_reply_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number ARP Replies transmitted

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_ARP_COUNTERS:
    """
    Return total Port ARP protocol statistics since last clear.
    """

    code: typing.ClassVar[int] = 727
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        invalid_arp_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of invalid ARP packets received
        arp_request_lookup_failure_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of ARP requests received that could not be resolved
        arp_reply_lookup_failure_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of ARP replies received that could not be resolved
        arp_request_retrans_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of retransmitted ARP requests
        arp_resolved_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of correct resolved IP addresses
        arp_failed_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of IP address that was not resolved
        arp_table_lookup_failure_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of dest IP addresses not found in the ARP table

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_NDP_RX_COUNTERS:
    """
    Return total Port NDP protocol receive statistics since last clear.
    """

    code: typing.ClassVar[int] = 728
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        ndp_request_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number NDP Requests received
        ndp_reply_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number NDP Replies received

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_NDP_TX_COUNTERS:
    """
    Return total Port NDP protocol transmit statistics since last clear.
    """

    code: typing.ClassVar[int] = 729
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        ndp_request_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number NDP Requests transmitted
        ndp_reply_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number NDP Replies transmitted

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_NDP_COUNTERS:
    """
    Return total Port NDP protocol statistics since last clear.
    """

    code: typing.ClassVar[int] = 730
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        invalid_ndp_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of invalid NDP packets received
        ndp_request_lookup_failure_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of NDP requests received that could not be resolved
        ndp_reply_lookup_failure_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of NDP replies received that could not be resolved
        ndp_request_retrans_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of retransmitted NDP requests
        ndp_resolved_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of correct resolved IP addresses
        ndp_failed_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of IP address that was not resolved
        ndp_table_lookup_failure_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of dest IP addresses not found in the NDP table

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_ICMP_RX_COUNTERS:
    """
    Return total Port ICMP protocol receive statistics since last clear.
    """

    code: typing.ClassVar[int] = 731
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        icmp_echo_reqest_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ICMP Echo requests received
        icmp_echo_reply_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ICMP Echo replies received
        icmp_dest_unknown_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ICMP Destination unknown received
        icmp_time_excessive_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ICMP Time exceeded received
        icmpv6_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ICMPv6 packets received

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_ICMP_TX_COUNTERS:
    """
    Return total Port ICMP protocol transmit statistics since last clear.
    """

    code: typing.ClassVar[int] = 732
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        icmp_echo_reqest_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ICMP Echo requests transmitted
        icmp_echo_reply_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ICMP Echo replies transmitted
        icmp_dest_unknown_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ICMP Destination unknown transmitted
        icmp_time_excessive_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ICMP Time exceeded transmitted
        icmpv6_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of ICMPv6 packets transmitted

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_ICMP_COUNTERS:
    """
    Return total Port ICMP protocol statistics since last clear.
    """

    code: typing.ClassVar[int] = 733
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        invalid_icmp_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of unknown or invalid ICMP packets received
        unknown_icmp_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of unknown or unsupported ICMP packets received
        invalid_icmpv6_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of unknown or invalid ICMPv6 packets received
        unknown_icmpv6_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of unknown or unsupported ICMPv6 packets received

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_TCP_RX_COUNTERS:
    """
    Return total Port TCP protocol receive statistics since last clear.
    """

    code: typing.ClassVar[int] = 734
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of TCP packets received

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_TCP_TX_COUNTERS:
    """
    Return total Port TCP protocol transmit statistics since last clear.
    """

    code: typing.ClassVar[int] = 735
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of TCP packets transmitted

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_TCP_COUNTERS:
    """
    Return total Port TCP protocol statistics since last clear.
    """

    code: typing.ClassVar[int] = 736
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        checksum_error_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of tcp packets which tcp header checksum error
        invalid_tcp_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of TCP packets which are malformed
        tcp_lookup_failure_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of TCP packets received that could not be resolved

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_UDP_RX_COUNTERS:
    """
    Return total Port UDP protocol receive statistics since last clear.
    """

    code: typing.ClassVar[int] = 737
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of UDP packets received

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_UDP_TX_COUNTERS:
    """
    Return total Port UDP protocol transmit statistics since last clear.
    """

    code: typing.ClassVar[int] = 738
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        packet_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of UDP packets transmitted

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_UDP_COUNTERS:
    """
    Return total Port UDP protocol statistics since last clear.
    """

    code: typing.ClassVar[int] = 739
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        checksum_error_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of udp packets which udp header checksum error
        invalid_udp_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, total number of UDP packets which are malformed
        udp_lookup_failure_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, number of UDP packets received that could not be resolved

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_CLEAR_COUNTERS:
    """
    Clears all run-time port counters.
    """

    code: typing.ClassVar[int] = 740
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class SetDataAttr:
        pass

    def set(self) -> "Token":
        return Token(
            self._connection,
            build_set_request(
                self,
                module=self._module,
                port=self._port,
            ),
        )


@register_command
@dataclass
class P4_ETH_COUNTERS:
    """
    Return total port Ethernet statistics since last clear.
    """

    code: typing.ClassVar[int] = 765
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        current_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, the current time (mSec since module restart)
        ref_time: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, reference time (mSec for P4_TRAFFIC on)
        tx_error_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, TX errors
        rx_error_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, RX errors
        rx_packet_lost_count: XmpField[XmpLong] = XmpField(XmpLong)  # long integer, packets lost by the Ethernet driver due to RX queue overflow

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_CLEAR:
    """
    Command to: Sets the Port State to OFF Delete all configured Connection Groups
    for the port No parameters
    """

    code: typing.ClassVar[int] = 766
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class SetDataAttr:
        pass

    def set(self) -> "Token":
        return Token(
            self._connection,
            build_set_request(
                self,
                module=self._module,
                port=self._port,
            ),
        )


@register_command
@dataclass
class P4_SPEEDSELECTION:
    """
    Sets the port speed. The selected speed must be one of the speeds supported by
    the port, which can be retrieved with P4_CAPABILITIES.
    """

    code: typing.ClassVar[int] = 767
    pushed: typing.ClassVar[bool] = True

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class SetDataAttr:
        speed: XmpField[XmpByte] = XmpField(XmpByte, choices=PortSpeed)  # coded byte, specifies the speed of the port

    @dataclass(frozen=True)
    class GetDataAttr:
        speed: XmpField[XmpByte] = XmpField(XmpByte, choices=PortSpeed)  # coded byte, specifies the speed of the port

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))

    def set(self, speed: PortSpeed) -> "Token":
        return Token(self._connection, build_set_request(self, module=self._module, port=self._port, speed=speed))

    set_auto = functools.partialmethod(set, PortSpeed.AUTO)
    set_f100m = functools.partialmethod(set, PortSpeed.F100M)
    set_f1g = functools.partialmethod(set, PortSpeed.F1G)
    set_f2_5g = functools.partialmethod(set, PortSpeed.F2_5G)
    set_f5g = functools.partialmethod(set, PortSpeed.F5G)
    set_f10g = functools.partialmethod(set, PortSpeed.F10G)
    set_f25g = functools.partialmethod(set, PortSpeed.F25G)
    set_f40g = functools.partialmethod(set, PortSpeed.F40G)
    set_f50g = functools.partialmethod(set, PortSpeed.F50G)
    set_f100g = functools.partialmethod(set, PortSpeed.F100G)


@register_command
@dataclass
class P4_MAX_PACKET_RATE:
    """
    Specifies the maximum number of packets per second allowed to be transmitted on
    the port.
    """

    code: typing.ClassVar[int] = 950
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class SetDataAttr:
        mode: XmpField[XmpByte] = XmpField(XmpByte, choices=AutoOrManual)  # coded byte, specifies the mode of the max. pps mechanism
        rate: XmpField[XmpInt] = XmpField(XmpInt)  # integer, maximum number of packets per second to transmit on this port
        time_window: XmpField[XmpInt] = XmpField(XmpInt)  # integer, time window [us] to measure the pps rate

    @dataclass(frozen=True)
    class GetDataAttr:
        mode: XmpField[XmpByte] = XmpField(XmpByte, choices=AutoOrManual)  # coded byte, specifies the mode of the max. pps mechanism
        rate: XmpField[XmpInt] = XmpField(XmpInt)  # integer, maximum number of packets per second to transmit on this port
        time_window: XmpField[XmpInt] = XmpField(XmpInt)  # integer, time window [us] to measure the pps rate

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))

    def set(self, mode: AutoOrManual, rate: int, time_window: int) -> "Token":
        return Token(self._connection, build_set_request(self, module=self._module, port=self._port, mode=mode, rate=rate, time_window=time_window))

    set_automatic = functools.partialmethod(set, AutoOrManual.AUTOMATIC)
    set_manual = functools.partialmethod(set, AutoOrManual.MANUAL)


@register_command
@dataclass
class P4_PCI_INFO:
    """
    Report the ports PCI info
    """

    code: typing.ClassVar[int] = 960
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        vendor_id: XmpField[XmpHex4] = XmpField(XmpHex4)  # four hex bytes, PCI Vendor ID
        device_id: XmpField[XmpHex4] = XmpField(XmpHex4)  # four hex bytes, PCI Device ID
        sub_vendor_id: XmpField[XmpHex4] = XmpField(XmpHex4)  # four hex bytes, PCI Subsystem Vendor ID
        sub_device_id: XmpField[XmpHex4] = XmpField(XmpHex4)  # four hex bytes, PCI Subsystem Device ID
        rev: XmpField[XmpInt] = XmpField(XmpInt)  # integer, Revision

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_FW_VER:
    """
    Report the firmware version of the port (NIC)
    """

    code: typing.ClassVar[int] = 961
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        major: XmpField[XmpInt] = XmpField(XmpInt)  # integer, Major firmware version
        minor: XmpField[XmpInt] = XmpField(XmpInt)  # integer, Minor firmware version

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_DEV_NAME:
    """
    Report the name of the device (NIC) on which the port is located.
    """

    code: typing.ClassVar[int] = 962
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        name: XmpField[XmpStr] = XmpField(XmpStr)  # string, name of the device (NIC) on which the port is located

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_PORT_TYPE:
    """
    Report the port type. The different possible ports are divided into types.
    """

    code: typing.ClassVar[int] = 963
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        type_number: XmpField[XmpInt] = XmpField(XmpInt)  # integer, enumerated port type
        type_string: XmpField[XmpStr] = XmpField(XmpStr)  # string, textual representation of the port type

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_LICENSE_INFO:
    """
    Returns information on the license assigned to the port - if any.
    """

    code: typing.ClassVar[int] = 964
    pushed: typing.ClassVar[bool] = True

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        present: XmpField[XmpByte] = XmpField(XmpByte, choices=IsPresent)  # coded byte, specifies if a license is assigned to the port
        speed: XmpField[XmpByte] = XmpField(XmpByte, choices=LicenseSpeed)  # coded byte, if a license is assigned to the port, specifies the speed of the license
        permanency: XmpField[XmpByte] = XmpField(XmpByte, choices=IsPermanent)  # coded byte, if a license is assigned to the port, specifies if the license is permanent
        expiration: XmpField[XmpLong] = XmpField(
            XmpLong
        )  # long integer, if a license is assigned to the port and it is not permanent, specifies the expiration date of the license - in seconds since Jan 1, 1970.

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


@register_command
@dataclass
class P4_APTITUDES:
    """
    Returns the ports aptitudes - i.e. what is possible to configure on the port in
    terms of features and performance. Current format of the bson document: key:
    chassis type: INT32 val: 2 key: tcp_udp type: DOCUMENT key: cc type: INT32 val:
    4000000 key: tls type: DOCUMENT key: supported type: BOOL val: true key: cc
    type: INT32 val: 200000 Where chassis has the following meaning: 0:
    CHASSIS_TYPE_UNKNOWN 1: CHASSIS_TYPE_APPLIANCE 2: CHASSIS_TYPE_BAY 3:
    CHASSIS_TYPE_COMPACT 4: CHASSIS_TYPE_SAFIRE
    """

    code: typing.ClassVar[int] = 1200
    pushed: typing.ClassVar[bool] = False

    _connection: "interfaces.IConnection"
    _module: int
    _port: int

    @dataclass(frozen=True)
    class GetDataAttr:
        bson: XmpField[XmpByteList] = XmpField(XmpByteList)  # list of hex bytes, bson document containing the ports aptitudes

    def get(self) -> "Token[GetDataAttr]":
        return Token(self._connection, build_get_request(self, module=self._module, port=self._port))


