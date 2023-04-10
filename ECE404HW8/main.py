from TcpAttack import * #Your TcpAttack class should be named as TcpAttack
 # Will contain actual IP addresses in real script
spoofIP="10.1.1.1" 
targetIP="128.46.4.101"
rangeStart= 1 
rangeEnd=1024
port=22
Tcp = TcpAttack(spoofIP,targetIP)
Tcp.scanTarget(rangeStart, rangeEnd)
if Tcp.attackTarget(port,10):
    print("port was open to attack")
 