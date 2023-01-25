import HandleFiles as hf
import os
import re

interpreter_version='v1'
name, instruction_list = hf.load_file(interpreter_version)

class Interpreter:
    def __init__(self):
        self.commands={
            # name: [nr of arguments to load, function to execute]
            'for': [2, self.handle_for],
            'rename': [2, self.handle_rename],
            'end': [0, self.handle_end]
        }
        self.types={
            '@dirs': os.path.isdir,
            '@file': os.path.isfile
        }
        self.keys_to_replace={
            '{@number}': '\d+',
            '{*}': '.*'
        }
    def handle_for(self, command_args):
        obj_to_search, name = command_args
        if obj_to_search != list(self.types.keys())[0] and obj_to_search != list(self.types.keys())[1]: # @dirs or @file
            raise ValueError('for does not support used type')
        working_dir=os.getcwd()
        for filename in os.listdir(working_dir):
            if not self.types[obj_to_search](filename):
                continue
            if not self.handle_name_check(filename, name):
                continue
            print(filename)

    def handle_name_check(self, name_to_check, checking_rule):
        for to_replace in list(self.keys_to_replace.keys()):
            checking_rule=checking_rule.replace(to_replace, self.keys_to_replace[to_replace])
        pattern=re.compile('^'+checking_rule+'$')
        return pattern.match(name_to_check) is not None


    def handle_rename(self):
        pass
    def handle_end(self):
        pass

    def execute_commands(self, parsed_istruct):
        command=parsed_istruct[0]
        if command in self.commands:
            command_args=parsed_istruct[1:self.commands[command][0] + 1]
            if len(command_args)!=self.commands[command][0]:
                raise ValueError('executed function does not have right amount of arguments')
            self.commands[command][1](command_args)
        else:
            raise ValueError(f'No function named {command}')

interpreter=Interpreter()

for instruction in instruction_list:
    instruction_parsed=instruction.split()
    Interpreter.execute_commands(interpreter, instruction_parsed)

