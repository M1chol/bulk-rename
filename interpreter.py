import HandleFiles as hf
import os

interpreter_version='v1'
name, instruction_list = hf.load_file(interpreter_version)
for instruction in instruction_list:
    pass