import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = []

# TARGET
target = Executable(
    script="run.py",
    base="gui",
    icon="favicon.ico"
)

# SETUP CX FREEZE
setup(
    name = "CalculusCalculator",
    version = "1.5.1",
    description = "微积分计算器v1.5.1",
    author = "LiMingkang",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
    
)
