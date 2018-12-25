import ifs
import os

class pyifs():

    def __init__(self,ldn):
        self.device = ifs.ifs(ldn.encode("utf-8"))

    def open(self,pathName,intFlag):
        fileObject = self.device.open(pathName.encode("utf-8"),intFlag.encode("utf-8"))
        return fileObject

    def close(self,fileObject):
        self.device.close(fileObject)

    def read(self,fileObject,size):
        data = self.device.read(fileObject,size)
        return data

    def write(self,fileObject,data,size):
        return self.device.write(fileObject,data,size)

    def flush(self,fileObject):
        return self.device.flush(fileObject)

    def seek(self,fileObject,offset,whence):
        return self.device.seek(fileObject,offset,whence)

    def tell(self,fileObject):
        return self.device.tell(fileObject)

    def mkdir(self,dirname):
        return self.device.mkdir(dirname.encode("utf-8"))

    def rmdir(self,dirname):
        return self.device.rmdir(dirname.encode("utf-8"))

    def opendir(self,dirname):
        dirObject = self.device.opendir(dirname.encode("utf-8"))
        return dirObject

    def readdir(self,dirObject):
        dir_entry = self.device.readdir(dirObject)
        return dir_entry

    def rename(self,old_name,new_name):
        self.device.rm(old_name.encode("utf-8"),new_name.encode("utf-8"))

    def copyToIfs(self, f, t):
        ff = open(f,'rb')
        ft = self.Open(t,'wb+')
        data = ff.read()
        self.write(ft,data,len(data))

        ff.close()
        self.close(ft)

    def copyFromIfs(self,f,t):
        ft = open(t,'wb+')
        ff = self.open(f,'rb')
        ff_len = self.seek(ff, 0,SEEK_END)
        self.seek(ff, 0,SEEK_SET)
        data = self.read(ff,ff_len)
        ft.write(data)

        ft.close()
        self.close(ff)

    def ls(self,dirname):
        dirObject = self.opendir(dirname)
        dirList = []
        if (dirObject):
            res = (0,'')
            while(res[0]==0):
                res = self.readdir(dirObject)
                if(res[0]==0):
                    dirList.append(res[1])
        return dirList
