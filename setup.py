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
    version = "1.6.0",
    description = "微积分计算器v1.6.0",
    author = "LiMingkang",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
    
)
