'prepare file for data saving
Set fso = CreateObject("Scripting.FileSystemObject")
'Set MyFile = fso.OpenTextFile("D:\asicAutoMeasurements\pawelLogParam.txt",8,True)

'clean previously created file
'fso.DeleteFile("D:\asicAutoMeasurements\waveform\*.txt")




'setting up lecroy oscilloscope
Set app = CreateObject("LeCroy.XStreamDSO")
app.Measure.MeasureMode = "MyMeasure"
'Set MyFile = fso.OpenTextFile("D:\asicAutoMeasurements\pawelLog.txt",8,True)
'ampl = 0.0




'app.Measure.ClearSweeps
'WScript.Sleep 3000 'wait for 3 sec
'ampl =  app.Measure.P1.mean.Result.value
'baseline = app.Measure.P3.mean.Result.value
'maxValue = app.Measure.P2.mean.Result.value
'MyFile.WriteLine( ampl & " " & baseline & " " & maxValue )

app.SaveRecall.Waveform.SaveTo = "File"
app.SaveRecall.Waveform.SaveSource = "C4"
app.SaveRecall.Waveform.WaveformDir = "D:\asicAutoMeasurements\waveform"
app.SaveRecall.Waveform.WaveFormat = "ASCII"
app.SaveRecall.Waveform.TraceTitle = "asic"
app.SaveRecall.Waveform.DoSave
WScript.Sleep 3000 'wait for 3 sec
'set trigger to auto in order to reset the waveform
app.Acquisition.TriggerMode = "Auto"
WScript.Sleep 1500 'wait for 0,5 sec
app.Acquisition.TriggerMode = "Normal"

'MyFile.Close
Set fso = Nothing
Set app = Nothing
'Wscript.Echo "Done"



