' this is comment
'this script read several measurements parameters from scope and put it to txt file

'setting up lecroy oscilloscope
Set app = CreateObject("LeCroy.XStreamDSO")
app.Measure.MeasureMode = "MyMeasure"
'variable to store parameters
width = 0.0


app.Measure.ClearSweeps
WScript.Sleep 500 'wait for 3 sec
width =  app.Measure.P1.Mean.Result.value

'DIM returnValue
'returnValue = width 
'WScript.Quit(returnValue)

Set app = Nothing
WScript.Echo width*10E8 
'WScript.Quit(returnValue)


