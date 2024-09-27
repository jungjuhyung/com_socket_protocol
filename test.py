import struct

array = bytes()
test1 = struct.pack("H", 7)
test2 = struct.pack("I", 1)
array = array + test1
array = array + test2

test3 = struct.pack("=HI", 7,1)

print(test3)
print(array)
