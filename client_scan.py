# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
"""
An example client. Run simpleserv.py first before running this.
"""
import time
import os

from twisted.internet import reactor, protocol
from ROOT import TCanvas    
from ROOT import TH1F
from ROOT import TFile
from ROOT import TGraph
from ROOT import TVector


# a client protocol
#flag = 0

value12b = 0

#f = TFile("testx_output.root","recreate");

def asicSet():
	global value12b
        upper = value12b & 4032
        upper = upper/64
        lower = value12b & 63#4032 
	cmd = "trbcmd w 0xe002 0xa000  0x521"+"{0:02x}".format(upper) 
	os.system(cmd)
	print 'asic set as: ' + cmd
	cmd = "trbcmd w 0xe002 0xa000  0x521"+"{0:02x}".format(lower) 
	os.system(cmd)
	print 'asic set as: ' + cmd
	print 'Current value ' + str(value12b)
	return value12b

class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def connectionMade(self):
	setting = asicSet()
	time.sleep(2)
        self.transport.write(str(setting)) #this is stransaction to scope, it will react by taking data and returning them

    def dataReceived(self, data):
        print "Server said:", data
	global value12b
	value12b += 1
	setting = asicSet()
	time.sleep(2)
	if (value12b < 4096):
		self.transport.write(str(setting))
	else:
	        self.transport.loseConnection()
	
    def connectionLost(self, reason):
        print "connection lost"

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


# this connects the protocol to a server running on port 8000
def main():
    os.system("trbcmd w 0xe002 0xa000 0x52014")
    time.sleep(1)
    f = EchoFactory()
    #reactor.connectTCP("localhost", 8001, f)
    reactor.connectTCP("192.168.0.6", 8001, f)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()

#for i in range(0,12):#iterate through all the registers
#        cmd =  " 1010010"+"{0:04b}".format(i)+"00000000"
        #h = TH1F("h1_"+cmd,"h1_"+cmd,100,0,100)
#        print "trbcmd w 0xe000 0xa000" + cmd
#        os.system("trbcmd w 0xe000 0xa000" + cmd)
#	flag = 0;
#	time.sleep(0.5)
#	while flag == 0:
#		None		
	#h.Fill(get_data())
        #h.Write()













