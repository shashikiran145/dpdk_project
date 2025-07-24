#!/bin/bash
for idx in $(seq 0 2); do
  i=$(($idx*2))
  j=$(($idx*2+1))
  intf0="veth$i"
  intf1="veth$j"

  if ip link show $intf0 > /dev/null; then
    ip link delete $intf0
  fi

  if ! ip link show $intf0 &> /dev/null; then
    ip link add name $intf0 type veth peer name $intf1
    #ip link set dev $intf0 up
    #ip link set dev $intf1 up
    ip link set address 02:00:00:00:00:0$idx dev $intf0 up
    ip link set address 02:00:00:00:01:0$idx dev $intf1 up
  fi
  sysctl net.ipv6.conf.$intf0.disable_ipv6=1
  sysctl net.ipv6.conf.$intf1.disable_ipv6=1
done
