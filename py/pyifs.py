import ifs
import os

class pyifs():

    def __init__(self,ldn):
        self.device = ifs.ifs(ldn.encode("utf-8"))
        
    def copy_to_ifs(self, f, t):
        ff = open(f,'rb')
        ft = self.device.open(t.encode("utf-8"),'wb+'.encode("utf-8"))
        data = ff.read()
        self.device.write(ft,data,len(data))
        
        ff.close()
        self.device.close(ft)
        
    def copy_from_ifs(self,f,t):
        ft = open(t,'wb+')
        ff = self.device.open(f.encode("utf-8"),'rb'.encode("utf-8"))
        ff_len = self.device.seek(ff, 0,SEEK_END)
        self.device.seek(ff, 0,SEEK_SET)
        data = self.device.read(ff,ff_len)
        ft.write(data)
        
        ft.close()
        self.device.close(ff)
        
    def mkdir(self,dir):
        self.device.mkdir(dir.encode("utf-8"))
        
    def ls(self,dir):
        self.device.readdir(dir.encode("utf-8"))
        
            