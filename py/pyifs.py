import ifs
import os

class pyifs():
    def __init__(self,img_name):
        self.drive = ifs.ifs(img_name.encode("utf-8"))
        self.path = self.drive.path

    def open(self,pathName,intFlag):
        fileObject = self.drive.open(pathName.encode("utf-8"),intFlag.encode("utf-8"))
        return fileObject

    def close(self,fileObject):
        self.drive.close(fileObject)

    def read(self,fileObject,size):
        data = self.drive.read(fileObject,size)
        return data

    def write(self,fileObject,data,size):
        return self.drive.write(fileObject,data,size)

    def flush(self,fileObject):
        return self.drive.flush(fileObject)

    def seek(self,fileObject,offset,whence):
        return self.drive.seek(fileObject,offset,whence)

    def tell(self,fileObject):
        return self.drive.tell(fileObject)

    def mkdir(self,dirname):
        return self.drive.mkdir(dirname.encode("utf-8"))

    def rmdir(self,dirname):
        return self.drive.rmdir(dirname.encode("utf-8"))

    def opendir(self,dirname):
        dirObject = self.drive.opendir(dirname.encode("utf-8"))
        return dirObject

    def readdir(self,dirObject):
        dir_entry = self.drive.readdir(dirObject)
        return dir_entry

    def rename(self,old_name,new_name):
        self.drive.rm(old_name.encode("utf-8"),new_name.encode("utf-8"))

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
            res = (0,'1')
            while((res[0]==0) and (len(res[1]) > 0)):
                res = self.readdir(dirObject)
                if((res[0]==0) and (len(res[1]) > 0)):
                    dirList.append(res[1:])
        return dirList
