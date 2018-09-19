import sys
from SCons.Script import *

os.system('mkdir -p sip/generated')
os.system('C:/Users/Administrator/Anaconda3/python.exe sip/configure.py')
os.system('cp /c/Users/Administrator/Anaconda3/libs/python36.lib /c/Users/Administrator/Anaconda3/libs/libpython36.a')


env = Environment(TOOLS=['as','gcc','g++','gnulink'])
objs = []
objs += Glob('fs/fatfs/*.c')
objs += Glob('sip/generated/*.cpp')
objs += Glob('sip/*.cpp')

env.Append(CPPPATH=['fs/fatfs','sip', 'sip/generated', 'c:/Users/Administrator/anaconda3/include'])
env.Append(CPPDEFINES=['_hypot=hypot'])
env.Append(LIBS=['python36'])
env.Append(LIBPATH=['/c/Users/Administrator/Anaconda3/libs'])

env.SharedLibrary('ifs.pyd', objs)
