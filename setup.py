import sys
from cx_Freeze import setup, Executable
exe = Executable(
    script=r"Collector.py",
    base="Win32GUI",
    )

setup(
    name = "Garbage Collector",
    version = "1.0",
    description = "Pick up trash",
    executables = [exe]
    )