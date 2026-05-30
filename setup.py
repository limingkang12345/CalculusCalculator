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
    version = "1.4.4",
    description = "微积分计算器v1.4.4",
    author = "LiMingkang",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
    
)
