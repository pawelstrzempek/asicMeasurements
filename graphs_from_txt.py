import os
from ROOT import TH1F
from ROOT import TFile
from ROOT import TGraph
from ROOT import TVector

path = r'./data/scan'  # remove the trailing '\'
f = TFile( path+"/waveforms_output.root" ,"recreate");
print 'Take data from ' + path
print 'Save output to ' + path+'waveforms_output.root'
#data = {}

def addDataToRootFile(data, name):
        #f = open('workfile_tmp.txt', 'a')
        #f.write(data)
        lines = data.split('\n')
#        print lines[0]
        x = TVector(len(lines)-1)
        y = TVector(len(lines)-1)
        for i in range(0,len(lines)-1):
                if(i > 4):
                        pair = lines[i].split(' ')
                        #
                        x[i] = float(pair[0])
                        y[i] = float(pair[1])
#			print 'x='+pair[0]+" y="+pair[1]
        g = TGraph(x,y)
        g.Write(str(name))
        print 'write graph'

for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    if os.path.isfile(dir_entry_path):
	if (dir_entry_path[-3:] =='txt'):#we look only for txt data files
	        with open(dir_entry_path, 'r') as my_file:
	#            data[dir_entry] = my_file.read()
	#	    print dir_entry
	#	    addDataToRootFile(str(data))
		    addDataToRootFile(my_file.read(),dir_entry)


