import HandleFiles as hf
import os
import re

interpreter_version='v1'
rs_file = hf.load_file(interpreter_version)

class Interpreter:
    def __init__(self):
        self.stack=[]
        self.items_in_loop=[]
        self.working_file=''
        self.commands={
            # name: [nr of arguments to load, function to execute]
            'for': [2, self.handle_for],
            'rename': [2, self.handle_rename],
            'end': [0, self.handle_end],
            'printloop': [0, self.printloop]
        }
        self.types={
            '@dirs': os.path.isdir,
            '@file': os.path.isfile
        }
        self.keys_to_replace={
            '{@number}': '\d+',
            '{*}': '.*'
        }
        self.renaming_vars={
            '{@original}': self.get_working_file_name,
            '{@parent}': self.get_working_dir
        }
    def handle_for(self):
        if self.items_in_loop: raise ValueError("Nested for loops not yet supported")
        obj_to_search, name = self.load_arguments(2)
        if obj_to_search != list(self.types.keys())[0] and obj_to_search != list(self.types.keys())[1]: # @dirs or @file
            raise ValueError("'for' does not support used type")
        working_dir=os.getcwd()
        files_in_loop=[]
        for filename in os.listdir(working_dir):
            if not self.types[obj_to_search](filename):
                continue
            if not self.handle_name_check(filename, name):
                continue
            files_in_loop.append(filename)
        self.items_in_loop=files_in_loop

    def handle_name_check(self, name_to_check, checking_rule):
        for to_replace in list(self.keys_to_replace.keys()):
            checking_rule=checking_rule.replace(to_replace, self.keys_to_replace[to_replace])
        pattern=re.compile('^'+checking_rule+'$')
        return pattern.match(name_to_check) is not None

    def printloop(self):
        print(self.items_in_loop)

    def handle_rename(self):
        old_name, new_name_rule = self.load_arguments(2)
        working_dir=os.getcwd()
        for dir in self.items_in_loop:
            os.chdir(working_dir+'\\'+dir)
            for filename in os.listdir(os.getcwd()):
                if not self.handle_name_check(filename, old_name):
                    continue
                new_name=new_name_rule
                self.working_file=filename
                for to_replace in list(self.renaming_vars.keys()):
                    new_name=new_name.replace(to_replace, self.renaming_vars[to_replace]())
                os.rename(filename, new_name)
            os.chdir(working_dir)

    def get_working_file_name(self): return self.working_file[:self.working_file.index('.')]
    def get_working_dir(self): return os.getcwd().split('\\')[-1]

    def handle_end(self):
        self.items_in_loop=[]

    def execute_command_on_stack(self):
        command=self.stack.pop(0)
        if command in self.commands:
            self.commands[command][1]()
        else:
            raise ValueError(f'No function named {command}')

    def load_commands_to_stack(self, list_of_commands):
        if self.stack: raise ValueError('Loaded to many arguments')
        self.stack=list_of_commands
        self.execute_command_on_stack()

    def load_arguments(self, number_of_arguments):
        if len(self.stack) < number_of_arguments: raise ValueError('Function tried to load too many arguments')
        if number_of_arguments==1: return self.stack.pop(0)
        to_ret=[]
        for i in range(number_of_arguments):
            to_ret.append(self.stack.pop(0))
        return to_ret


interpreter=Interpreter()

for line_nr, instruction in enumerate(rs_file):
    instruction_parsed=instruction.split()
    try:
        Interpreter.load_commands_to_stack(interpreter, instruction_parsed)
    except ValueError as encountered_error:
        print(f'{hf.Bcolors.FAIL}{rs_file.name} failed on line {line_nr+1} with error: {encountered_error}{hf.Bcolors.ENDC}')
        quit()
