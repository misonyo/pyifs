import pyifs

device = pyifs.pyifs("1:")

#file1 = device.open("hello.txt".encode("utf-8"),"r+".encode("utf-8"))

#result = device.read(file1,24)

#print("xxxx")
#print("result is :",result)

dir1 = device.opendir("1:/")
print("dir1 :",dir1)
res = device.readdir(dir1)

print("readdir:",res)

print(device.ls("1:/"))
