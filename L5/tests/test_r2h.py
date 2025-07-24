import ptf
from ptf.base_tests import BaseTest
from ptf import config, mask
from ptf import packet as scapy
import ptf.testutils as testutils

class TestClass(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        self.dataplane = ptf.dataplane_instance

    def tearDown(self):
        BaseTest.tearDown(self)

class TestPacketIdentificationAndRemoval(TestClass):
    def runTest(self):
        pktlen = 100
        pkt = testutils.simple_tcp_packet(pktlen=pktlen,
            eth_src='02:00:00:00:00:04',
            eth_dst='02:00:00:00:00:02',
            ip_src='10.0.0.6', ip_dst='10.0.0.4',
            ip_ttl=9, tcp_sport=35681, tcp_dport=80)

        testutils.send_packet(self, 0, pkt)
        
        exp = mask.Mask(pkt)
        exp.set_do_not_care_scapy(scapy.TCP, "chksum")
        exp.set_do_not_care_scapy(scapy.IP, "chksum")
        exp.set_do_not_care_scapy(scapy.IP, "ihl")
        exp.set_do_not_care_scapy(scapy.IP, "len")

        testutils.verify_packet(self, exp, 2)  # Verify packet is sent to host

class TestForwardingToNextHop1(TestClass):
    def runTest(self):
        pktlen = 100
        pkt = testutils.simple_tcp_packet(pktlen=pktlen,
            eth_src='02:00:00:00:00:04',
            eth_dst='02:00:00:00:00:02',
            ip_src='10.0.0.6', ip_dst='10.0.0.5',  # Non-target IP
            ip_ttl=9, tcp_sport=35681, tcp_dport=80)

        testutils.send_packet(self, 0, pkt)

        exp = mask.Mask(pkt)
        exp.set_do_not_care_scapy(scapy.TCP, "chksum")
        exp.set_do_not_care_scapy(scapy.IP, "chksum")
        exp.set_do_not_care_scapy(scapy.IP, "ihl")
        exp.set_do_not_care_scapy(scapy.IP, "len")

        testutils.verify_packet(self, exp, 1)  # Verify at the next hop

class TestForwardingToNextHop2(TestClass):
    def runTest(self):
        pktlen = 100
        pkt = testutils.simple_tcp_packet(pktlen=pktlen,
            eth_src='02:00:00:00:00:04',
            eth_dst='02:00:00:00:00:02',
            ip_src='10.0.0.6', ip_dst='10.0.0.5',  # Non-target IP
            ip_ttl=9, tcp_sport=35681, tcp_dport=80)

        testutils.send_packet(self, 1, pkt)

        exp = mask.Mask(pkt)
        exp.set_do_not_care_scapy(scapy.TCP, "chksum")
        exp.set_do_not_care_scapy(scapy.IP, "chksum")
        exp.set_do_not_care_scapy(scapy.IP, "ihl")
        exp.set_do_not_care_scapy(scapy.IP, "len")

        testutils.verify_packet(self, exp, 0)  # Verify at the next hop