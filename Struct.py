import struct

im
print dir(struct)
a = 20
b = 400

str = struct.pack('ii',a,b)

print 'length',len(str)
print str
print repr(str)