from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("main.py", base=base)]

packages = ["idna"]
options={"build_exe": {"include_files": "main.ui"}}
executables=executables,


setup(
name="mytest",
version="0.1",
description="",
options={"build_exe": {"include_files": "main.ui"}},
executables=[Executable("main.py")],
)


