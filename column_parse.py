

##This is the python script wich reads the data from file (two columns separated with space and with sereval (4) lines at the beginning of the file)
## and creates the ROOT graph out of the data

from ROOT import TGraph 
from ROOT import TCanvas 
from ROOT import TVector 


c = TCanvas()
f = open('testbenchFile.txt','r')
buf = f.read();
f.close()
lines = buf.split('\n')
print lines[0]
x = TVector(len(lines)-1)
y = TVector(len(lines)-1)

for i in range(0,len(lines)-1):
	if(i > 4):
		pair = lines[i].split(' ')
		print 'x='+pair[0]+" y="+pair[1]
		#x.append(float(pair[0]))
		#y.append(float(pair[1]))
		x[i] = float(pair[0])
		y[i] = float(pair[1])
		
		
#print 'X:\n' + x
#print 'Y:\n' + y
print "\n\n"
print x[20]


g = TGraph(x,y)
g.Draw()

s = raw_input('--> ')
#print y

#data = numpy.genfromtxt(buffer, delimiter = ',')

#graf = TGraph()

