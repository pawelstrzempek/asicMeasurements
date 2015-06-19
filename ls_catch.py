import subprocess
import os
#proc = subprocess.Popen('trbcmd r 0xe002 0xa000', stdout=subprocess.PIPE)
#tmp = proc.stdout.read()
tmp = os.popen('trbcmd r 0xe002 0xa000').read()
print ">"+tmp[-3:-1]+"<"
