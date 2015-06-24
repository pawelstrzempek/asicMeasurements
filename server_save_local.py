__author__ = 'ps'

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import time
import os
import glob


from twisted.internet import reactor, protocol


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        print "I have received: " + str(data)
        payload = collect_scope_data(data)
        print 'I collect the data and save it'
        self.transport.write('ack')
        print 'Job done'


#def collect_scope_data():
#    """this function triggers the script for waveform collection"""
#   os.system('scope_action.py 1') #sc_waveform file generation
#    scopeData = ""
#    f = open('sc_waveform', 'r')
#    scopeData = f.read()
#    return scopeData

def collect_scope_data(name):
    """this function triggers the script for waveform collection"""
    callscript = 'waveformToDisk_leaveFile.vbs '+name
    os.system(callscript) #sc_waveform file generation
    time.sleep(1)
    scopeData = ""
    #fileName = glob.glob('D:/asicAutoMeasurements/waveform/*')
    #f = open(str(fileName[0]), 'r')
    #scopeData = f.read()
    return scopeData
    #return str(fileName[0])



def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8001,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()



##        time.sleep(1)
##        print '10'
##        time.sleep(1)
##        print '9'
##        time.sleep(1)
##        print '8'
##        time.sleep(1)
##        print '7'
##        time.sleep(1)
##        print '6'
##        time.sleep(1)
##        print '5'
##        time.sleep(1)
##        print '4'
##        time.sleep(1)
##        print '3'
##        time.sleep(1)
##        print '2'
##        time.sleep(1)
##        print '1'
