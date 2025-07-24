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

class TestARPFlooding0(TestClass):
    def runTest(self):
        # Creating an ARP request packet
        arp_req = testutils.simple_arp_packet(
            arp_op=1,  # 1 for ARP request
            pktlen=60,  # Typical ARP packet length
            hw_snd='02:00:00:00:00:01',  # Sender's hardware address
            ip_snd='10.0.0.4',  # Sender's IP address
            hw_tgt='00:00:00:00:00:00',  # Target hardware address (unknown for ARP request)
            ip_tgt='10.0.0.5'  # Target IP address
        )

        # Sending the ARP request packet on port 2
        testutils.send_packet(self, 0, arp_req)

        # Expecting the same ARP packet on ports 0 and 1
        exp = mask.Mask(arp_req)
        exp.set_do_not_care_scapy(scapy.Ether, "dst")

        # Verify the packet is being flooded on ports 0 and 1
        testutils.verify_packet(self, exp, 1)
        testutils.verify_packet(self, exp, 2)

class TestARPFlooding1(TestClass):
    def runTest(self):
        arp_req = testutils.simple_arp_packet(
            arp_op=1,
            pktlen=60,
            hw_snd='02:00:00:00:00:01',
            ip_snd='10.0.0.4',
            hw_tgt='00:00:00:00:00:00',
            ip_tgt='10.0.0.5'
        )

        testutils.send_packet(self, 1, arp_req)

        exp = mask.Mask(arp_req)
        exp.set_do_not_care_scapy(scapy.Ether, "dst")

        testutils.verify_packet(self, exp, 0)
        testutils.verify_packet(self, exp, 2)

class TestARPFlooding2(TestClass):
    def runTest(self):
        arp_req = testutils.simple_arp_packet(
            arp_op=1,
            pktlen=60,
            hw_snd='02:00:00:00:00:01',
            ip_snd='10.0.0.4',
            hw_tgt='00:00:00:00:00:00',
            ip_tgt='10.0.0.5'
        )

        testutils.send_packet(self, 2, arp_req)

        exp = mask.Mask(arp_req)
        exp.set_do_not_care_scapy(scapy.Ether, "dst")

        testutils.verify_packet(self, exp, 0)
        testutils.verify_packet(self, exp, 1)