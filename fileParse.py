import glob

def collect_scope_data():
    """this function triggers the script for waveform collection"""
    #os.system('scope_action.py 1') #sc_waveform file generation
    scopeData = ""
    fileName = glob.glob('D:/asicAutoMeasurements/waveform/*')
    f = open(str(fileName[0]), 'r')
    scopeData = f.read()
    return scopeData
    #return str(fileName[0])

print collect_scope_data()
