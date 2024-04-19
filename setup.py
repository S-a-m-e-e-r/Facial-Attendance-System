import sys
from cx_Freeze import setup,Executable
import os
build_exe_options={"packages":["os"],"excludes":["Tkinter"]}
base=None
if sys.platform=='win32':
    base='Win32GUI'

setup(name='Face-Detect',
      version='1.0.0',
      author='The_6_boys',
      description="Our project work",
      options={"build_exe":build_exe_options},
      executables=[Executable('GUi3.py',base=base,
                        shortcutName="Face-Detect",
                        icon=r"pictures/guifoo.ico",
                        shortcutDir="DesktopFolder")])
