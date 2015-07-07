import os
import subprocess
from ROOT import TH1F
from ROOT import TFile
from ROOT import TGraph
from ROOT import TCanvas
from ROOT import TVector

path = r'./dataWaveformsCompare'  # remove the trailing '\'
f = TFile( path+"/th1f_from_txt_output.root" ,"recreate");
print 'Take data from ' + path
print 'Save output to ' + path+'waveforms_output.root'
#data = {}

BINS = 1001
MIN_BIN = -4.33386e-008
MAX_BIN = 1.56861e-007
h_buf =  TH1F("h","h",BINS,MIN_BIN,MAX_BIN);
flag = 0

def addDataToRootFile(data, name):
        global flag
	global h_buf
	#f = open('workfile_tmp.txt', 'a')
        #f.write(data)
        lines = data.split('\n')
#        print lines[0]
        x = TVector(len(lines)-1)
        y = TVector(len(lines)-1)
	h = TH1F("h","h",BINS,MIN_BIN,MAX_BIN)
        for i in range(0,len(lines)-1):
                if(i > 4):
                        pair = lines[i].split(' ')
                        #
			h.SetBinContent(i,float(pair[1]));
                        #x[i] = float(pair[0])
                        #y[i] = float(pair[1])
#			print 'x='+pair[0]+" y="+pair[1]
        #g = TGraph(x,y)
        if (flag == 0):
		h_buf = h
		flag = 1
	else:
		c = TCanvas()
		c.cd()
		h.Draw()
		h_buf.Draw("same")
		flag = 0
		c.Write()	
	#h.Write(str(name))
        print 'write graph'

#for dir_entry in os.listdir(path):
#    dir_entry_path = os.path.join(path, dir_entry)
#    if os.path.isfile(dir_entry_path):
#	if (dir_entry_path[-3:] =='txt'):#we look only for txt data files
#	        with open(dir_entry_path, 'r') as my_file:
#		    addDataToRootFile(my_file.read(),dir_entry)

tmp = (os.popen('ls -lhtr '+path).read()).split('\n')
#print ">"+str(tmp)+"<"+str(len(tmp))


for i in range(0, len(tmp)):
	 if ((tmp[i])[-3:] =='txt'):
              print tmp[i]                 


