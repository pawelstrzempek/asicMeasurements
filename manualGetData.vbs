' this is comment
'this script read several measurements parameters from scope and put it to txt file

'setting up lecroy oscilloscope
Set app = CreateObject("LeCroy.XStreamDSO")
app.Measure.MeasureMode = "MyMeasure"
'variable to store parameters
ampl = 0.0
baseline = 0.0
maxValue = 0.0

'prepare file for data saving
Set fso = CreateObject("Scripting.FileSystemObject")
Set MyFile = fso.OpenTextFile("D:\asicAutoMeasurements\pawelLogParam.txt",8,True)



app.Measure.ClearSweeps
WScript.Sleep 3000 'wait for 3 sec
ampl =  app.Measure.P1.mean.Result.value
baseline = app.Measure.P3.mean.Result.value
maxValue = app.Measure.P2.mean.Result.value
MyFile.WriteLine( ampl & " " & baseline & " " & maxValue )




MyFile.Close
Set fso = Nothing
Set app = Nothing
Wscript.Echo "Done"



