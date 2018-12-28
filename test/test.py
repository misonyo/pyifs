import pyifs

device = pyifs.pyifs("1:")

file1 = device.open("1:/main.c","r")
print(">>>file1:",file1)
result = device.read(file1,500)

print(">>>read result:",result)

result = device.read(file1,24)

print(">>>read result:",result)

result = device.read(file1,24)

print(">>>read result:",result)

dir1 = device.opendir("1:/")
print(">>>dir1 :",dir1)
res = device.readdir(dir1)

print(">>>readdir:",res)

print(device.ls("1:/"))
