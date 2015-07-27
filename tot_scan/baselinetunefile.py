import os
import sys
import time
import glob
import numpy #for median calulation
from ROOT import TH1F
from ROOT import TH2F
from ROOT import TFile
from ROOT import TGraph
from ROOT import TCanvas


##CONFIGURATION:          #####
ch_min=1 #dont start from 0
ch_max=49
confFile = "./feb_conf_org.txt"
workPath = ""
unpackerXml = "/home/pandastraws/Unpacker/tools2/conf_trb3_panda.xml"
cailbConf = "/home/pandastraws/Unpacker/tools2/xx15202135949.hld_paramsGOLDEN.root"

###############################

channelMeanTabel=range(ch_max);
#channelMeanTabel.zeros(ch_max)


def collectData():
	global workPath
        time.sleep(1)
        os.system("daq_evtbuild -m 1 -d file -o "+workPath+"  -q 128 &")
        os.system("daq_netmem -m 1 -i UDP:127.0.0.1:50000 -q 128 &")
        time.sleep(15)
        os.system("killall -9 daq_evtbuild")
        os.system("killall -9 daq_netmem")
        time.sleep(1)



def readRootFile(ch_min, ch_max,filePath):
	global channelMeanTabel;
	print filePath
	rootFile = TFile(filePath)
	for i in range(ch_min,ch_max):
		h = TH1F()
		h = (rootFile.Get("tot_hist_ch"+str(i)))
		h.Draw()
		channelMeanTabel[i] = h.GetMean()
	print channelMeanTabel

def readConfFile(filename):
        filename= open(filename, 'r')
        dataBlock = filename.read()
        lines = dataBlock.split('\n')
        while (len(lines) != 0 and lines[0][0] != '%' ):
                lines.pop(0);
        lines.pop(0) #get rid of the line with marker %
        return lines



def updateBaselines(ch_min,ch_max,confFileName):
	global channelMeanTabel
	median = numpy.median(numpy.array(channelMeanTabel))
	confData = readConfFile(confFileName)
        for i in range(ch_min, ch_max):
		cmdBuffor = dataChToRegNum(i)#0xe002 0xa000 0x52(channelNumber)
		print "\n\n=====>Processing channel:"+str(i)
#		cmdBuffor = "0xe000 0xa000 0x52a"
		if(cmdBuffor == ""):#omitting ref channels
			continue
		#We get the current value of a register (baseline) from configuration file
		for d in range(0,len(confData)):
			if(cmdBuffor == confData[d][:-2]):
				#print cmdBuffor + " | " +confData[d][:-2]
        	        	baselineLvl = int(confData[d][-2:],16)# hex string to int 
				print "d[-2:] "+ confData[d][-2:]+ "  " + str(baselineLvl)
				'''Now we make decision if increase or decreas the baseline'''
				if(channelMeanTabel[i] > (median+0.5)):#means that our tot is above median so we lower baseline
					print "Inc. Median: "+str(median)+"\t tot: "+str(channelMeanTabel[i])+"\t cmdWd: "+"trbcmd w " + cmdBuffor + "%0.2x" % (baselineLvl-1)
					confData[d] = confData[d][:-2] + "%0.2x" % (baselineLvl-1)
					
				#	os.system("trbcmd w " + cmdBuffor + str(hex(baselineLvl-1))[-2:])
					os.system("trbcmd w " + cmdBuffor + "%0.2x" % (baselineLvl-1))
					time.sleep(1)
				#	os.system("trbcmd w " + cmdBuffor + str(hex(baselineLvl-1))[-2:])
					os.system("trbcmd w " + cmdBuffor + "%0.2x" % (baselineLvl-1))
					time.sleep(1)
				elif(channelMeanTabel[i] < (median-0.5)):
					print "Dec. Median: "+str(median)+"\t tot: "+str(channelMeanTabel[i])+"\t cmdWd: "+"trbcmd w " + cmdBuffor + "%0.2x" % (baselineLvl+1)
					confData[d] = confData[d][:-2] + "%0.2x" % (baselineLvl+1)
					
					#os.system("trbcmd w " + cmdBuffor + str(hex(baselineLvl+1))[-2:])
					os.system("trbcmd w " + cmdBuffor + "%0.2x" % (baselineLvl+1))
					time.sleep(1)
					#os.system("trbcmd w " + cmdBuffor + str(hex(baselineLvl+1))[-2:])
					os.system("trbcmd w " + cmdBuffor + "%0.2x" % (baselineLvl+1))
					time.sleep(1)
				else:
					print "Sta. Median: "+str(median)+"\t tot: "+str(channelMeanTabel[i])+"\t cmdWd: "+"trbcmd w " + cmdBuffor + "%0.2x" % (baselineLvl)
					confData[d] = confData[d][:-2] + "%0.2x" % (baselineLvl)
					
					#os.system("trbcmd w " + cmdBuffor + str(hex(baselineLvl))[-2:])
					os.system("trbcmd w " + cmdBuffor + "%0.2x" % (baselineLvl))
					time.sleep(1)
					#os.system("trbcmd w " + cmdBuffor + str(hex(baselineLvl))[-2:])
					os.system("trbcmd w " + cmdBuffor + "%0.2x" % (baselineLvl))
					time.sleep(1)
				break #we found the channel so we stop iteration through the channel list form config file
		print "next\n\n"

	f = open(confFileName)
	file_str = f.read() # read it in as a string, Not line by line
	f.close()
	#file_str[file_str.find("%"):] = "" #deleting rest of the file
	file_str = file_str.replace(file_str[file_str.find("%")+1:],  "") #deleting rest of the file
	file_str += "\n"
	for b in range(0,len(confData)-1):
		file_str += str(confData[b]+"\n" )
#	print file_str
	#
	# do_actions_on_file_str
	#
	f = open(confFileName, 'w') # to clear the file
	f.write(file_str)
	f.close()	


def dataChToRegNum(channel):
	'''The assumption is that we have 192 channels divided to 4 TDC each 48 channels ( + ref ch )'''
	if(channel == 0 or channel == 49 or channel == 98 or channel == 147):
		return ""
	if(channel >0 and channel < 49):
		if(channel > 0 and channel < 9):
			return "0xe000 0xa000 0x52" + str(hex(channel+3))[-1:]
		if(channel > 8 and channel < 17):
			return "0xe000 0xa000 0x54" + str(hex(channel-5))[-1:]
		if(channel > 16 and channel < 25):
			return "0xe000 0xa000 0xd2" + str(hex(channel-13))[-1:]
		if(channel > 24 and channel < 33):
		        return "0xe000 0xa000 0xd4" + str(hex(channel-21))[-1:]
		if(channel > 32 and channel < 41):
			return "0xe000 0xa000 0x152"+ str(hex(channel-29))[-1:]
		if(channel > 40 and channel < 49):
			return "0xe000 0xa000 0x154"+ str(hex(channel-37))[-1:]
        if(channel >49 and channel < 98):
		channel = channel -49;
                if(channel > 0 and channel < 9):
                        return "0xe001 0xa000 0x52" + str(hex(channel+3))[-1:]
                if(channel > 8 and channel < 17):                              
                        return "0xe001 0xa000 0x54" + str(hex(channel-5))[-1:]
                if(channel > 16 and channel < 25):                             
                        return "0xe001 0xa000 0xd2" + str(hex(channel-13))[-1:]
                if(channel > 24 and channel < 33):                             
                        return "0xe001 0xa000 0xd4" + str(hex(channel-21))[-1:]
                if(channel > 32 and channel < 41):                             
                        return "0xe001 0xa000 0x152"+ str(hex(channel-29))[-1:]
                if(channel > 40 and channel < 49):                             
                        return "0xe001 0xa000 0x154"+ str(hex(channel-37))[-1:]
        if(channel >98 and channel < 147):
                channel = channel -98;
                if(channel > 0 and channel < 9):
                        return "0xe002 0xa000 0x52" + str(hex(channel+3))[-1:]
                if(channel > 8 and channel < 17):                              
                        return "0xe002 0xa000 0x54" + str(hex(channel-5))[-1:]
                if(channel > 16 and channel < 25):                             
                        return "0xe002 0xa000 0xd2" + str(hex(channel-13))[-1:]
                if(channel > 24 and channel < 33):                             
                        return "0xe002 0xa000 0xd4" + str(hex(channel-21))[-1:]
                if(channel > 32 and channel < 41):                             
                        return "0xe002 0xa000 0x152"+ str(hex(channel-29))[-1:]
                if(channel > 40 and channel < 49):                             
                        return "0xe002 0xa000 0x154"+ str(hex(channel-37))[-1:]
        if(channel >147 and channel < 197):
                channel = channel -147;
                if(channel > 0 and channel < 9):
                        return "0xe003 0xa000 0x52" + str(hex(channel+3))[-1:]
                if(channel > 8 and channel < 17):                              
                        return "0xe003 0xa000 0x54" + str(hex(channel-5))[-1:]
                if(channel > 16 and channel < 25):                             
                        return "0xe003 0xa000 0xd2" + str(hex(channel-13))[-1:]
                if(channel > 24 and channel < 33):                             
                        return "0xe003 0xa000 0xd4" + str(hex(channel-21))[-1:]
                if(channel > 32 and channel < 41):                             
                        return "0xe003 0xa000 0x152"+ str(hex(channel-29))[-1:]
                if(channel > 40 and channel < 49):                             
                        return "0xe003 0xa000 0x154"+ str(hex(channel-37))[-1:]
	return ""


def init():
	if(len(sys.argv) != 2 ):
		print "Give operation path as an argument.\n"
		sys.exit(0)
	else:
		global workPath
		workPath = sys.argv[1] 	



init()
for rounds in range(0,14):
	collectData()
	newest = max(glob.iglob(workPath+'*.hld'), key=os.path.getctime)
	os.system('root -l -q -l -b \'/home/pandastraws/Unpacker/tools2/launcher_run_analysis.c(10000,"' +newest+ '","'+unpackerXml +'",149,"'+cailbConf+'")\'')
	newest = max(glob.iglob(workPath+'*histos.root'), key=os.path.getctime)
	print "========> "+newest
	readRootFile(ch_min, ch_max,newest)
	updateBaselines(ch_min, ch_max,confFile)
#for i in range (0,200):
#	print dataChToRegNum(i)


