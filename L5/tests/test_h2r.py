import ptf
from ptf.base_tests import BaseTest
from ptf import config, mask
from ptf import packet as scapy
import ptf.testutils as testutils

all_ports = [0, 1, 2]

class TestClass(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        self.dataplane = ptf.dataplane_instance

    def tearDown(self):
        BaseTest.tearDown(self)

class TestHostToRingForwarding(TestClass):
    def runTest(self):
        pktlen = 100
        pkt = testutils.simple_tcp_packet(pktlen=pktlen,
            eth_src='02:00:00:00:00:01',  # Host source
            eth_dst='02:00:00:00:00:02',  # First hop in the ring
            ip_src='10.0.0.4', ip_dst='10.0.0.5',  # From host to non-target IP
            ip_ttl=9, tcp_sport=35681, tcp_dport=80)

        testutils.send_packet(self, 2, pkt)

        exp = mask.Mask(pkt)
        exp.set_do_not_care_scapy(scapy.TCP, "chksum")
        exp.set_do_not_care_scapy(scapy.IP, "chksum")
        exp.set_do_not_care_scapy(scapy.IP, "ihl")
        exp.set_do_not_care_scapy(scapy.IP, "len")

        testutils.verify_packet(self, exp, 0)  # Verify packet is being flooded
        testutils.verify_packet(self, exp, 1)