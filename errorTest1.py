#!/usr/bin/python
import random
import time
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
	global h_rece, h_send, h_rece2
	h_send.Write();
	h_rece.Write();
	h_rece2.Write();
	f.Close();
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



def get_data():
	x = random.randrange(0, 101, 2)
	return x;

c = TCanvas()
f = TFile("test1_output.root","recreate");
h_send = TH1F("h_send","h1_send",12,0,12)
h_rece = TH1F("h_rece","h1_rece",12,0,12)
h_rece2 = TH1F("h_rece2","h1_rece2",12,0,12)
"""Iterating through the registers"""
"""ASIC1"""
while 1:
	for i in range(0,12):
		print 'Testing reg nb ' + format(i,'x')
		cmd =  " 0xD2"+format(i,'x')+"1f"
		print "trbcmd w 0xe000 0xa000" + cmd	
		os.system("trbcmd w 0xe000 0xa000" + cmd)
		time.sleep(1)
		os.system("trbcmd w 0xe000 0xa000" + cmd)
		h_send.Fill(i);
		time.sleep(1)
		#proc = subprocess.Popen('trbcmd r 0xe000 0xa000', stdout=subprocess.PIPE)
		#tmp = proc.stdout.read()
		tmp = os.popen('trbcmd r 0xe000 0xa000').read()
		#print ">"+tmp[-3:-1]+"< compare with >"+"1f<"
		if(tmp[-3:-1] == "1f"):
			h_rece.Fill(i)
		else:
			pass
		#cmd =  " 1010010"+"{0:04b}".format(i)+"00011111"
		cmd =  " 0xD2"+format(i,'x')+"1f"
                print "trbcmd w 0xe000 0xa000" + cmd
                os.system("trbcmd w 0xe000 0xa000" + cmd)
                time.sleep(1)
                #proc = subprocess.Popen('trbcmd r 0xe000 0xa000', stdout=subprocess.PIPE)
                #tmp = proc.stdout.read()
		tmp = os.popen('trbcmd r 0xe000 0xa000').read()
                if(tmp[-3:-1] == "1f"):
                        h_rece2.Fill(i)
                else:
                        pass


                #cmd =  " 1010010"+"{0:04b}".format(i)+"00010011"
		cmd =  " 0xD2"+format(i,'x')+"13"
                print "trbcmd w 0xe000 0xa000" + cmd
                os.system("trbcmd w 0xe000 0xa000" + cmd)
		time.sleep(1)
		os.system("trbcmd w 0xe000 0xa000" + cmd)
                h_send.Fill(i);
                time.sleep(1)
                #proc = subprocess.Popen('trbcmd r 0xe000 0xa000', stdout=subprocess.PIPE)
                #tmp = proc.stdout.read()
                tmp = os.popen('trbcmd r 0xe000 0xa000').read()
		if(tmp[-3:-1] == "13"):
                        h_rece.Fill(i)
                else:
                        pass
                #cmd =  " 1010010"+"{0:04b}".format(i)+"00010011"
		cmd =  " 0xD2"+format(i,'x')+"13"
                print "trbcmd w 0xe000 0xa000" + cmd
                os.system("trbcmd w 0xe000 0xa000" + cmd)
                time.sleep(1)
                #proc = subprocess.Popen('trbcmd r 0xe000 0xa000', stdout=subprocess.PIPE)
                #tmp = proc.stdout.read()
                tmp = os.popen('trbcmd r 0xe000 0xa000').read()
		if(tmp[-3:-1] == "13"):
                        h_rece2.Fill(i)
                else:
                        pass

       	#	h.Fill(get_data())
	#	h.Write()
	
#"""ASIC2"""
#for i in range(0,12):
#	print "trbcmd w 0xe000 0xa000" + " 1010100"+"{0:04b}".format(i)+"00000000"	



