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

reg_index = 0
name_index = 0

f = TFile("testx_output.root","recreate");

def asicSet():
	global reg_index
	cmd = "trbcmd w 0xe002 0xa000  0x52"+format(reg_index,'x')+"1f"
	ret_value = '0x52'+format(reg_index,'x')+'1f'
	os.system(cmd)
	print 'asic set as: ' + cmd
	reg_index += 1
	if (reg_index == 12):
		reg_index = 0
	return ret_value

def addDataToFile(data,nameIndex):
	#f = open('workfile_tmp.txt', 'a')
	#f.write(data)
	lines = data.split('\n')
	#print lines[0]
	x = TVector(len(lines)-1)
	y = TVector(len(lines)-1)

	for i in range(0,len(lines)-1):
	        if(i > 4):
	                pair = lines[i].split(' ')
	                #print 'x='+pair[0]+" y="+pair[1]
	                #x.append(float(pair[0]))
	                #y.append(float(pair[1]))
	                x[i] = float(pair[0])
	                y[i] = float(pair[1])
	g = TGraph(x,y)
	g.Write()
	print 'write graph'




class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def connectionMade(self):
	setting = asicSet()
	time.sleep(2)
        self.transport.write(setting) #this is stransaction to scope, it will react by taking data and returning them

    def dataReceived(self, data):
        print "Server said:", data
	global name_index
	name_index += 1
	#addDataToFile(data, name_index)
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













