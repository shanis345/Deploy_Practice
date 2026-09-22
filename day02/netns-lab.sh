#!/usr/bin/env bash
# Day 2 실습 2-1~2-4 를 한 번에 (Linux/WSL2, sudo 필요). 여러 번 실행해도 안전.
#   ./netns-lab.sh        : 만들기 + 검증
#   ./netns-lab.sh clean  : 정리
set -u
clean() {
  sudo pkill -f "nc -l -k 10.42.0.20" 2>/dev/null
  sudo iptables -D FORWARD -i br-lab -j ACCEPT 2>/dev/null
  sudo iptables -D FORWARD -o br-lab -j ACCEPT 2>/dev/null
  sudo iptables -t nat -D POSTROUTING -s 10.42.0.0/24 ! -o br-lab -j MASQUERADE 2>/dev/null
  sudo ip netns del biz 2>/dev/null; sudo ip netns del db 2>/dev/null; sudo ip link del br-lab 2>/dev/null
  echo "정리 완료"
}
[ "${1:-}" = "clean" ] && { clean; exit 0; }
clean >/dev/null
sudo ip netns add biz; sudo ip netns add db
sudo ip link add br-lab type bridge && sudo ip addr add 10.42.0.1/24 dev br-lab && sudo ip link set br-lab up
for pair in "veth-biz biz 10.42.0.10" "veth-db db 10.42.0.20"; do
  set -- $pair
  sudo ip link add "$1" type veth peer name eth0 netns "$2"
  sudo ip link set "$1" master br-lab && sudo ip link set "$1" up
  sudo ip netns exec "$2" ip addr add "$3/24" dev eth0
  sudo ip netns exec "$2" ip link set eth0 up && sudo ip netns exec "$2" ip link set lo up
  sudo ip netns exec "$2" ip route add default via 10.42.0.1
done
sudo iptables -I FORWARD -i br-lab -j ACCEPT; sudo iptables -I FORWARD -o br-lab -j ACCEPT
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null
sudo iptables -t nat -A POSTROUTING -s 10.42.0.0/24 ! -o br-lab -j MASQUERADE
echo "== biz → db"; sudo ip netns exec biz ping -c1 -W1 10.42.0.20 | tail -1
echo "== biz → 인터넷 (TCP 443)"; sudo ip netns exec biz nc -zv -w3 1.1.1.1 443
echo "== 라우팅"; sudo ip netns exec biz ip route
