from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import arp, ipv4, ipv6
from ryu.lib.packet import icmp, tcp, udp
from ryu.lib.packet import ether_types
from ryu.lib.packet import in_proto
import time


class Simple_switch_13_dl(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Simple_switch_13_dl, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.mac_to_port = {
            1: {
                "00:00:00:00:00:a1": 3,
                "00:00:00:00:00:b1": 4,
                "00:00:00:00:00:a3": 2,
                "00:50:56:ed:d2:93": 1,
                "00:00:00:00:00:01": 4294967294,
                "b8:ac:6f:36:1c:a2": 3,
                "b8:ac:6f:36:07:cf": 4,
            }
        }

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
        self.add_flow(0, datapath, 0, match, actions)

    def add_flow(self, idle_t, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            idle_timeout=idle_t,
            instructions=inst,
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        _priority = 100
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        arp_pkt = pkt.get_protocol(arp.arp)
        ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
        icmp_pkt = pkt.get_protocol(icmp.icmp)
        tcp_pkt = pkt.get_protocol(tcp.tcp)
        udp_pkt = pkt.get_protocol(udp.udp)

        if eth_pkt.ethertype in set(
            [
                0x6558,
                0x6558,
                0x8100,
                0x86DD,
                0x8809,
                0x8847,
                0x88A8,
                0x88CC,
                0x88E7,
                0x88E7,
                0x05DC,
                0x8902,
                0x894F,
            ]
        ):
            return

        in_port = msg.match["in_port"]

        self.mac_to_port[dpid][eth_pkt.src] = in_port

        if eth_pkt.dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][eth_pkt.dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        if out_port != ofproto.OFPP_FLOOD:
            if eth_pkt.ethertype == ether_types.ETH_TYPE_ARP:
                _priority = 30
                match = parser.OFPMatch(
                    in_port=in_port,
                    eth_type=eth_pkt.ethertype,
                    eth_src=eth_pkt.src,
                    eth_dst=eth_pkt.dst,
                    arp_spa=arp_pkt.src_ip,
                    arp_tpa=arp_pkt.dst_ip,
                    arp_op=arp_pkt.opcode,
                )

            elif eth_pkt.ethertype == ether_types.ETH_TYPE_IPV6:
                return

            elif eth_pkt.ethertype == ether_types.ETH_TYPE_IP:
                if ipv4_pkt.proto == in_proto.IPPROTO_ICMP:
                    match = parser.OFPMatch(
                        in_port=in_port,
                        eth_type=eth_pkt.ethertype,
                        eth_src=eth_pkt.src,
                        eth_dst=eth_pkt.dst,
                        ipv4_src=ipv4_pkt.src,
                        ipv4_dst=ipv4_pkt.dst,
                        ip_proto=ipv4_pkt.proto,
                        icmpv4_type=icmp_pkt.type,
                        icmpv4_code=icmp_pkt.code,
                    )
                elif ipv4_pkt.proto == in_proto.IPPROTO_TCP:
                    match = parser.OFPMatch(
                        in_port=in_port,
                        eth_type=eth_pkt.ethertype,
                        eth_src=eth_pkt.src,
                        eth_dst=eth_pkt.dst,
                        ipv4_src=ipv4_pkt.src,
                        ipv4_dst=ipv4_pkt.dst,
                        ip_proto=ipv4_pkt.proto,
                        tcp_src=tcp_pkt.src_port,
                        tcp_dst=tcp_pkt.dst_port,
                    )
                elif ipv4_pkt.proto == in_proto.IPPROTO_UDP:
                    match = parser.OFPMatch(
                        in_port=3,
                        eth_type=eth_pkt.ethertype,
                        eth_src=eth_pkt.src,
                        eth_dst=eth_pkt.dst,
                        ipv4_src=ipv4_pkt.src,
                        ipv4_dst=ipv4_pkt.dst,
                        ip_proto=ipv4_pkt.proto,
                        udp_src=udp_pkt.src_port,
                        udp_dst=udp_pkt.dst_port,
                    )
                else:
                    return

            else:
                return

            self.add_flow(10, datapath, _priority, match, actions)

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=ofproto.OFP_NO_BUFFER,
            in_port=in_port,
            actions=actions,
            data=msg.data,
        )

        datapath.send_msg(out)