#!/usr/bin/python
import random
import time
import thread
from ROOT import TCanvas        # available at startup
from ROOT import TH1F
from ROOT import TFile



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

def get_data():
	x = random.randrange(0, 101, 2)
	return x;

c = TCanvas()
f = TFile("code.root","recreate");

"""Iterating through the registers"""
"""ASIC1"""
for i in range(0,12):
	cmd =  " 1010010"+"{0:04b}".format(i)+"00000000"
	h = TH1F("h1_"+cmd,"h1_"+cmd,100,0,100)
	print "trbcmd w 0xe000 0xa000" + cmd	
        h.Fill(get_data())
	h.Write()
	
#"""ASIC2"""
#for i in range(0,12):
#	print "trbcmd w 0xe000 0xa000" + " 1010100"+"{0:04b}".format(i)+"00000000"	







