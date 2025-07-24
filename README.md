# dpdk_project

DPDK project used inside the SDN lecture VM

# Scenario
Given the following hardware setup:

Multiple workstations are equipped with 2-port 100G QSFP network interface cards (NICs).
You want to be able to communicate with each workstation from each workstation, but you do
not have a switch available. You connect the workstations in a ring-topology, where the two
ports of the NIC connect to two other workstations. You use DPDK to implement transparent forwarding
and routing. Each packet sent to the ring is not modified in any way, and is delivered to the
respective host by inspecting the IP-address. These IP-addresses are assigned statically to each
workstation. Additionally, each workstation has a virtual ethernet interface set up, which connects
to the DPDK application as well, and allows the host the send and recieve packets via this interface.

Within DPDK, three ports are connected to your application:

- Port 0 and 1, which correspond to the ports of the NIC, i.e. the Ring
- Port 2 which binds to the virtual ethernet interface, i.e. your workstation

# Tasks
## Task 1: ARP support
To be able to ping others, IP addresses have to be resolved into MAC addresses. To achieve this, your
code should inspect the ethertype of incoming packets. Whenever it is the ethertype is ARP, the packet
should be broadcasted on all ports, except the port that it was recieved. A more complete implementation
of the ARP protocol is not required.

## Task 2: Ring to Host Communication
To be able to send packets over the ring and recieve packets from the ring, your application should inspect
the packets ethertype if it is an IPv4 packet. If this is the case, check the target IP-address. If it is the
IP address configured for your host (which is configured via the CONFIGURED_IP constant, where CONFIGURED_IP = 4
is equal to 10.0.0.4), the packet should be sent to port 2. If not, the packet should be send to the opposite port
of the ring, so a packet recieved on port 0 should be sent to port 1.

## Task 3: Host to Ring Communication
To send packets to other hosts, your code should again inspect the ethertype. If the packet is an IPv4 packet and
the destination address is not your own, and the packet was recieved on port 2, the packet should be send to both
port 0 and 1, i.e. broadcasted to the ring.

# Running the application
- Terminal 1: `./run_dpdk.sh` (it will start the environment, build the project and run the app)
- Terminal 2: `./run_test.sh` (runs the tests)  
  You can add `test_arp`, `test_r2h` or `test_h2r` as parameter to only run the test for the tasks. Or even with the test name e.g `./run_test.sh test_arp.TestARPFlooding0`  
  For a full list of tests run `./run_test.sh --list`

# Hints
- You can use the `#define LOG printf` to get some debug output (see top of file)
- The DPDK headers are in `/usr/local/include/`. You might want to look at the `rte_ip.h` for the IP packet.

[See slide 53 of lecture 17.12.]
Information about DPDK: [http://doc.dpdk.org/guides/sample_app_ug/skeleton.html]

TODO: rewrite MAC address?
