#!/usr/bin/python
import random
import time
import datetime
import thread
from ROOT import TCanvas        # available at startup
from ROOT import TH1F
from ROOT import TFile

import signal
import sys
import subprocess
import os 
# 0x52 .... -conn 1
# 0xD2 .... -conn 2

# Define a function for the thread
#def print_time( threadName, delay):
#   count = 0
#   while count < 5:
#      time.sleep(delay)
#      count += 1
#      print "%s: %s" % ( threadName, time.ctime(time.time()) )

# Create two threads as follows
#try:
#   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
#except:
#   print "Error: unable to start thread"

#while 1:
#   pass
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
	global f
	global h_rece, h_send 
	h_send.Write();
	h_rece.Write();
	f.Close();
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



def get_data():
	x = random.randrange(0, 101, 2)
	return x;


def readInData(filename):
	filename= open(filename, 'r')
	dataBlock = filename.read()
	lines = dataBlock.split('\n')
	return lines

def getfilename():
	filename = ""
	if(len(sys.argv)==2):
		filename = sys.argv[1]
		print filename
	else:
		print 'usage: python errorTest1b.py file\nwhere file contains list of register to be set in format: 0xe000 0xa000 0x52011'
		sys.exit(1) 
	return filename


data = readInData(getfilename())

c = TCanvas()
f = TFile("test1b_output.root","recreate");
h_send = TH1F("h_send","h1_send",len(data),0,len(data))
h_rece = TH1F("h_rece","h1_rece",len(data),0,len(data))

h_send.Draw()
h_rece.SetLineColor(3)
h_rece.Draw("same")

startPoint = datetime.datetime.now()
print startPoint;
while 1:
	#reseting Asics
	os.system("trbcmd w 0xe000 0xa000 0x300000")
	time.sleep(1)
	os.system("trbcmd w 0xe000 0xa000 0x280000")
	time.sleep(1)
	os.system("trbcmd w 0xe000 0xa000 0x200000")
	time.sleep(1)
	os.system("trbcmd w 0xe001 0xa000 0x280000")
	time.sleep(2)
	for i in range(0,len(data)-1):
		print 'Testing reg '+str(i+1)+'/'+str(len(data)-1)+' : ' + data[i]
#		cmd =  " 0xD2"+format(i,'x')+"1f"
#		print "trbcmd w 0xe000 0xa000" + cmd	
		os.system("trbcmd w " + data[i])
		time.sleep(1)
		os.system("trbcmd w " + data[i])
		time.sleep(1)
		h_send.Fill(i);
#		#proc = subprocess.Popen('trbcmd r 0xe000 0xa000', stdout=subprocess.PIPE)
#		#tmp = proc.stdout.read()
		tdcAddr = data[i][data[i].find("0xe")+3:data[i].find("0xe")+6]
		tmp = os.popen('trbcmd r 0xe'+tdcAddr+' 0xa000').read()
		#tmp = "abcd"
#		print ">"+tmp[-3:-1]+"< compare with >"+data[i][-2:]+"<"
		if(tmp[-3:-1] == data[i][-2:]):
			h_rece.Fill(i)
		else:
			pass
		print 'got:                     ' + tmp 
		currentTime = datetime.datetime.now()
		if((startPoint - currentTime).seconds > 300):#backup every 5 min
        		h_send.Write()
        		h_rece.Write()
		h_send.Draw()
                h_rece.Draw("same")
		c.Update()




#		#cmd =  " 1010010"+"{0:04b}".format(i)+"00011111"
#		cmd =  " 0xD2"+format(i,'x')+"1f"
#                print "trbcmd w 0xe000 0xa000" + cmd
#                os.system("trbcmd w 0xe000 0xa000" + cmd)
#                time.sleep(1)
#                #proc = subprocess.Popen('trbcmd r 0xe000 0xa000', stdout=subprocess.PIPE)
#                #tmp = proc.stdout.read()
#		tmp = os.popen('trbcmd r 0xe000 0xa000').read()
#                if(tmp[-3:-1] == "1f"):
#                        h_rece2.Fill(i)
#                else:
#                        pass
#
#
