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


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def readInData(filename):
	filename= open(filename, 'r')
	dataBlock = filename.read()
	lines = dataBlock.split('\n')
	while (len(lines) != 0 and lines[0][0] != '%' ):
		lines.pop(0);
	lines.pop(0) #get rid of the line with marker %
	return lines

def getfilename():
	filename = ""
	if(len(sys.argv)== 3 and (sys.argv[1] == '-s' or sys.argv[1] == '-c')):
		filename = sys.argv[2]
		print filename
	else:
		print 'usage: python setFEb.py -option file\n		       file contains list of register to be set in format: 0xe000 0xa000 0x52011\n                  option is equal to -s (set FEBs) or -c (check FEBs)\n'
		sys.exit(1) 
	return filename


def findTDCaddr(inputData):
	TDCaddr = []
	TDCaddr.append(inputData[0][0:6])
	for i in range(0,len(inputData)-1):
		if(TDCaddr[-1] != inputData[i][0:6]):
			TDCaddr.append(inputData[i][0:6])
	return TDCaddr



def update_progress(progress, progress_max):
    sys.stderr.write( '\r[{}] {:.2%}'.format('#'*((progress/progress_max)*10), (float(progress)/float(progress_max)) ))

def asicReset(tdcaddr):
	print tdcaddr
	for j in range(0,len(tdcaddr)):
		os.system('trbcmd w '+tdcaddr[j]+' 0xa000 0x300000')
		#print 'trbcmd w '+tdcaddr[j]+' 0xa000 0x300000'
		time.sleep(1)
		os.system('trbcmd w '+tdcaddr[j]+' 0xa000 0x280000')
		#print 'trbcmd w '+tdcaddr[j]+' 0xa000 0x300000'
		time.sleep(1)
		os.system('trbcmd w '+tdcaddr[j]+' 0xa000 0x200000')
		#print  'trbcmd w '+tdcaddr[j]+' 0xa000 0x300000'
		time.sleep(1)



data = readInData(getfilename())
if(data[0][0:2] != '0x'):# a bit naive check but better than none
	print 'Wrong input file format!\n'
	sys.exit(0)
startPoint = datetime.datetime.now()
print startPoint;
#print findTDCaddr(data)
#reseting Asics
#ta = findTDCaddr(data)
errorTable = []
if(sys.argv[1] == '-s'):
	asicReset(findTDCaddr(data))
	for i in range(0,len(data)-1):
		update_progress(i+1,len(data)-1)
		os.system("trbcmd w " + data[i])
		#print "trbcmd w " + data[i]
		time.sleep(1)
		os.system("trbcmd w " + data[i])
		time.sleep(1)
elif(sys.argv[1] == '-c'):
        for i in range(0,len(data)-1):
                update_progress(i+1,len(data)-1)
                os.system("trbcmd w " + data[i])
		#print 'trbcmd r '+data[i][0:13]
                tmp = os.popen('trbcmd r '+data[i][0:6]+' 0xa000').read()
		if(tmp[-3:-1] != data[i][-2:]):
                        #print 'Error at: ' + data[i] +'\n read: '+ tmp;
			errorTable.append('Error at: ' + data[i] +'\n read: '+ tmp+'\n')
                else:
                        pass
                os.system("trbcmd w " + data[i])
                time.sleep(1)
                os.system("trbcmd w " + data[i])
                time.sleep(1)	
else:
	print 'Wrong option! Select -s or -c\n'
print "\n\n"
if(len(errorTable) != 0):
	print errorTable


print 'Seconds elapsed: '+str((datetime.datetime.now() - startPoint).seconds)



