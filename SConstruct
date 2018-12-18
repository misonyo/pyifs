import sys
from SCons.Script import *

os.system('mkdir -p sip/generated')
os.system('C:/Anaconda3/python.exe sip/configure.py')
os.system('cp /c/Anaconda3/libs/python36.lib /c/Anaconda3/libs/libpython36.a')


env = Environment(TOOLS=['as','gcc','g++','gnulink'])
objs = []
objs += Glob('fs/fatfs/*.c')
objs += Glob('sip/generated/*.cpp')
objs += Glob('sip/*.cpp')

env.Append(CPPPATH=['fs/fatfs','sip', 'sip/generated', 'c:/anaconda3/include'])
env.Append(CPPDEFINES=['_hypot=hypot'])
env.Append(LIBS=['python36'])
env.Append(LIBPATH=['/c/Anaconda3/libs'])

env.SharedLibrary('py/ifs.pyd', objs)
