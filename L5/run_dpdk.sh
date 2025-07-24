#!/bin/bash

cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"

echo "Building DPDK application"
# rebuild C application
make clean
make || exit 1

# setup virtual interfaces
sudo ./tests/veth_setup.sh

# check if hugepages alredy present
if [ `cat /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages` -lt 1024 ]
then
	echo 1024 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages >/dev/null
	sudo mkdir /mnt/huge
	sudo mount -t hugetlbfs nodev /mnt/huge
fi

echo "Running DPDK application"
# run DPDK application
sudo ./build/lab5 --vdev=eth_af_packet0,iface=veth1 --vdev=eth_af_packet1,iface=veth3 --vdev=eth_af_packet2,iface=veth5
