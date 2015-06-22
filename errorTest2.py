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
from ROOT import TObject


# a client protocol
#flag = 0

reg_value = 0

f = TFile("test2_output.root","recreate")
h_result = TH1F("h_result","h_result",12,-2,10)
c = TCanvas()
h_result.Draw()

def asicSet():
	global reg_value
	if (reg_value == 0): # we send narrow setting
		cmd = "trbcmd w 0xe002 0xa000  0x52011" #30 ns
		ret_value = '0x52011'
		os.system(cmd)
		print 'asic set as: ' + cmd
		reg_value = 1 # next time we send wide
	else:
		cmd = "trbcmd w 0xe002 0xa000  0x52013" #80 ns
		ret_value = '0x52013'
		os.system(cmd)
		print 'asic set as: ' + cmd
		reg_value = 0 # next time we send narrow

	return ret_value


class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def connectionMade(self):
	setting = asicSet()
	time.sleep(2)
        self.transport.write(setting) #this is stransaction to scope, it will react by taking data and returning them

    def dataReceived(self, data):
        print "Server said:", data #incoming data format : measured_pulse_width-reg_value
	buf = data.split('-');
	print 'parse data: buf[0]=' + buf[0] + '| buf[1]=' + buf[1] +'|' 
#	if (float(buf[0])>20 and float(buf[0])<40):
#		print  float(buf[0])  
	if(buf[1] == '0x52011' and float(buf[0]) >20 and float(buf[0])<40):#everything ok
		h_result.Fill(6)
		h_result.Write("",TObject.kOverwrite)
		c.Update()
	elif (buf[1] == '0x52013' and float(buf[0]) >50 and float(buf[0])<100):
                h_result.Fill(6)
                h_result.Write("",TObject.kOverwrite)
                c.Update()
	else:
		h_result.Fill(0)
		h_result.Write("",TObject.kOverwrite)
		c.Update()

	#and we repead the operation
	setting = asicSet()
	time.sleep(2)
	self.transport.write(setting)


#        self.transport.loseConnection()

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
    f = EchoFactory()
#    reactor.connectTCP("localhost", 8001, f)
    reactor.connectTCP("192.168.0.6", 8001, f)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()





