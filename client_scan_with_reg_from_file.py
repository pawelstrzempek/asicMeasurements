# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
"""
An example client. Run simpleserv.py first before running this.
"""
import time
import os
import signal
import sys
import subprocess

from twisted.internet import reactor, protocol
from ROOT import TCanvas    
from ROOT import TH1F
from ROOT import TFile
from ROOT import TGraph
from ROOT import TVector


# a client protocol
#flag = 0

resetIteration = 10
currentIndex = 0
regValTable_A = []
regValTable_B = []

#f = TFile("testx_output.root","recreate");

def readInData(filename):
        filename= open(filename, 'r')
        dataBlock = filename.read()
        lines = dataBlock.split('\n')
        return lines

def getfilename(whichFile):#1 or 2
        filename = ""
        if(len(sys.argv)==3):
                filename = sys.argv[whichFile]
                print filename
        else:
                print 'usage: python client_scan_with_reg_from_file.py file_A file_B\nwhere file contains list of register to be set in format: 0xe000 0xa000 0x52011'
                sys.exit(1)
        return filename



def asicSet():
	global regValTable_A
	global regValTable_B
	global resetIteration 
	if (resetIteration % 2 == 0):
		regValTable = regValTable_A	
	else:
		regValTable = regValTable_B

	asicIterator = 0;
	for asicIterator in range(0, (len(regValTable))/12):
		cmd = "trbcmd w " + regValTable[currentIndex+asicIterator*12]
		os.system(cmd)
		os.system(cmd)
		time.sleep(1)
		print 'asic set as: ' + cmd 
		print 'Current index value ' + str(currentIndex+asicIterator*12)
	return  (regValTable[currentIndex])[-7:]

class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def connectionMade(self):
	setting = asicSet()
	time.sleep(2)
        self.transport.write(str(setting)) #this is stransaction to scope, it will react by taking data and returning them

    def dataReceived(self, data):
        print "Server said:", data
	global resetIteration 
	global currentIndex 
	currentIndex += 1
	if (currentIndex == 12):
		currentIndex =0
		resetIteration -=1
	time.sleep(5)
	setting = asicSet()
	time.sleep(2)
	if (resetIteration != 0):
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
    global regValTable_A
    global regValTable_B
    regValTable_A = readInData(getfilename(1))
    regValTable_B = readInData(getfilename(2))
    """RESETING all 3 FEBs"""
    os.system("trbcmd w 0xe000 0xa000 0x300000")
    time.sleep(1)
    os.system("trbcmd w 0xe000 0xa000 0x280000")
    time.sleep(1)
    os.system("trbcmd w 0xe000 0xa000 0x200000")
    time.sleep(2)
    os.system("trbcmd w 0xe001 0xa000 0x280000")
    time.sleep(2)


    f = EchoFactory()
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













