

for i in range(0,4095):
	upper = i & 4032
	lower = i & 63#4032 
	upper = upper/64
	#print "{0:012b}".format(i) + ' = u:' + "{0:06b}".format(upper) +" l:"+ "{0:06b}".format(lower)
	print "{0:012b}".format(i) + ' = u:' + "{0:02x}".format(upper) +" l:"+ "{0:02x}".format(lower)
