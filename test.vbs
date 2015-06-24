'Wscript.Sleep 1000
'MsgBox "TEST"

'ampl = 0.01

'Do Until ampl = 0.05
'	ampl = ampl + 0.01
'	MsgBox "TEST" & ampl
'	WScript.Sleep 5000
'Loop

Set app = CreateObject("LeCroy.XStreamDSO")

amplituda = 0

app.Measure.MeasureMode = "MyMeasure"
app.Measure.ClearSweeps
amplituda =  app.Measure.P1.mean.Result.value
'MsgBox amplituda


app.Acquisition.Trigger.C3.Level = 1.656
WScript.Sleep 5000



app.Acquisition.Trigger.C3.Level = 2.0
ampl = 0.1
	If ampl = 0.1 Then
		MsgBox ampl
		app.Acquisition.Trigger.C3.Level = 1.656		
	End If	