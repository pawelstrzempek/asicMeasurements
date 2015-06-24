' this is comment
'starting constraints
lowAmp = 0.795'0.01
highAmp = 1.4'0.18
step = 0.005
lowTrig = 2.0'1.630'1.591 '1.628'1.656
highTrig = 2.0'1.800 '1.950'2.0


'setting up lecroy oscilloscope
Set app = CreateObject("LeCroy.XStreamDSO")
app.Measure.MeasureMode = "MyMeasure"
'variable to store input amplitude
ampl = lowAmp
'and output amplitude
amplP1mean = 0.0
tot = 0.0
sdev = 0.0
'following lines are neede for program excecution
Dim objShell
Set objShell = WScript.CreateObject( "WScript.Shell" )
'prepare file for data saving
Set fso = CreateObject("Scripting.FileSystemObject")
Set MyFile = fso.OpenTextFile("D:\asicAutoMeasurements\pawelLog.txt",8,True)
'set initial trigger low to cath low amplitude
app.Acquisition.Trigger.C3.Level = lowTrig

Do Until ampl >= highAmp
	If ampl >= 0.05 Then	
		app.Acquisition.Trigger.C3.Level = highTrig		
	End If	
	objShell.Run("D:\asicAutoMeasurements\generator.exe " & ampl)
	ampl = ampl + step
	WScript.Sleep 1000
	app.Measure.ClearSweeps
	WScript.Sleep 7000 'wait for 7 sec
	'acquire mean of output amplitude
	amplP1mean =  app.Measure.P1.mean.Result.value
	tot =  app.Measure.P2.mean.Result.value
	sdev =  app.Measure.P2.sdev.Result.value
	MyFile.WriteLine( ampl & " " & amplP1mean & " " & tot & " " & sdev )
Loop


MyFile.Close
Set fso = Nothing
Set app = Nothing
Set objShell = Nothing




