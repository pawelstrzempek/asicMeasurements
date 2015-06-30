import datetime
import time
import random
from ROOT import TH1F
from ROOT import TFile
from ROOT import TCanvas


strDate = datetime.datetime.now()
hist = TH1F("hist",""+str(strDate),100000,0,100000)
c = TCanvas()
hist.Draw()

while True:
	i = random.randint(1, 100)
	curDate = datetime.datetime.now()
	hist.SetBinContent((curDate-strDate).seconds,i)
#	time.sleep(random.randint(1, 10))
	time.sleep(1)
	
