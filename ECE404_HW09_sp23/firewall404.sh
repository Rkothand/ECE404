#Homework number:09
#Name: Rohith Kothandaraman
#ECN login: rkothand
#due date: 3/28/2023

#flush and delete all previous rules
sudo iptables -t filter -F
sudo iptables -t filter -X
sudo iptables -t mangle -F
sudo iptables -t mangle -X
sudo iptables -t nat -F
sudo iptables -t nat -X
sudo iptables -t raw -F
sudo iptables -t raw -X

#only accept packets from f1.com
sudo iptable -A INPUT -p tcp --dport 80 -s f1.com -j ACCEPT

# For all outgoing packets, change their source IP address to your own machine’s IP address
sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE

# Write a rule to protect yourself against indiscriminate and nonstop scanning of ports on your machine

sudo iptables -A FORWARD -p tcp --tcp-flags SYN,ACK,FIN,RST NONE -m limit --limit 1/s -j ACCEPT

# Write a rule to protect yourself from a SYN-flood Attack by limiting the number of incoming
sudo iptables -A FORWARD -p tcp --syn -m limit --limit 500 -j ACCEPT

# Write a rule to allow full loopback access on your machine i.e. access using localhost
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT

# Write a port forwarding rule that routes all traffic arriving on port 8888 to port 25565
sudo iptables -t nat -A PREROUTING -p tcp --dport 8888 -j DNAT --to-destination 25565

# Write a rule that only allows outgoing ssh connections to engineering.purdue.edu. You
# will need two rules, one for the INPUT chain and one for the OUTPUT chain on the FILTER
# table
sudo iptables -A INPUT -p tcp --dport 22 -s engineering.purdue.edu -m state --state NEW,ESTABLISHED -j ACCEPT

sudo iptables -A OUTPUT -p tcp --sport 22 -d engineering.purdue.edu -m state --state ESTABLISHED -j ACCEPT

# Drop any other packets if they are not caught by the above rules
sudo iptables -A INPUT -j DROP
sudo iptables -A OUTPUT -j DROP
sudo iptables -A FORWARD -j DROP
