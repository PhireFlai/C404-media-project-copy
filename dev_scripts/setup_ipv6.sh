#!/bin/bash

# 1. Configure Docker daemon.json with nano editor
sudo tee /etc/docker/daemon.json <<EOF
{
  "experimental": true,
  "ip6tables": true,
  "ipv6": true,
  "fixed-cidr-v6": "fd00:dead:beef::/64"
}
EOF

# 2. Enable IPv6 forwarding
sudo sysctl -w net.ipv6.conf.all.forwarding=1
sudo sysctl -p

# 3. Restart Docker
sudo systemctl restart docker

# 4. Verify NAT configuration and addresses
echo -e "\nNAT Configuration:"
sudo ip6tables -t nat -L -n -v

echo -e "\nGlobal IPv6 Addresses:"
ip -6 addr show scope global

# 5. Start services
docker compose up --build -d

# # 6. Verification steps
# echo -e "\nContainer IPv6 Address:"
# docker inspect my_container | grep IPv6Address

# echo -e "\nTesting connectivity:"
# DB_IPV6=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.GlobalIPv6Address}}{{end}}' db 2>/dev/null)
# HOST_IPV6=$(ip -6 addr show scope global | grep -oP '(?<=inet6 )[\da-f:]+' | head -n1 | cut -d'/' -f1)

# echo "Host IPv6: $HOST_IPV6"
# echo "DB Container IPv6: $DB_IPV6"

# echo -e "\nPort 8000 Listening:"
# sudo ss -tulpn | grep 8000

# echo -e "\nPing Tests:"
# docker exec w25-project-cyan-backend-1 ping6 -c 4 $DB_IPV6
# docker exec w25-project-cyan-backend-1 ping6 -c 4 ipv6.google.com

# # 7. Cleanup
# docker compose down