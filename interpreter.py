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
        self.file_counter=0
        self.local_file_counter=0
        self.base_working_dir=''
        self.suppresed_question=False
        self.override_delete_from_stack=False
        self.commands={
            # name: function to execute, number of arguments
            'for': [self.handle_for, 2],
            'rename': [self.handle_file_rename, 2],
            'end': [self.handle_end, 0],
            'printloop': [self.printloop, 0],
            'del': [self.handle_file_delete, 1],
            'reset_counter': [self.handle_reset_counter, 0]
        }
        self.types={
            '@dirs': os.path.isdir,
        }
        self.keys_to_replace={
            '{@number}': '\d+',
            '{*}': '.*'
        }
        self.renaming_vars={
            '{@original}': self.get_working_file_name,
            '{@parent}': self.get_working_dir,
            '{@counter}': self.handle_counter,
            '{@l_counter}': self.handle_l_counter
        }
    def handle_for(self):
        if self.items_in_loop: raise ValueError("Nested for loops not yet supported")
        obj_to_search, name = self.load_arguments(self.commands['for'][1])
        if obj_to_search != list(self.types.keys())[0]: # @dirs
            raise ValueError("'for' does not support used type")
        files_in_loop=[]
        for filename in os.listdir(self.base_working_dir):
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
        command_name='printloop'
        print(self.items_in_loop)
        input('Press any key to continue...')
        return self.commands[command_name][1]

    def handle_file_rename(self): self.handle_file_loop(self.rename_files)
    def handle_file_delete(self): self.handle_file_loop(self.delete_files)

    def handle_file_loop(self, function_to_exec):
        if not self.items_in_loop:
            function_to_exec(os.listdir(self.base_working_dir))
        else:
            self.override_delete_from_stack=True
            nr_to_del=0
            for dirs in self.items_in_loop:
                os.chdir(self.base_working_dir + '\\' + dirs)
                nr_to_del=function_to_exec(os.listdir(os.getcwd()))
                os.chdir(self.base_working_dir)
            del self.stack[:nr_to_del]
            self.override_delete_from_stack=False

    def rename_files(self, working_dir_list):
        command_name='rename'
        old_name, new_name_rule=self.load_arguments(self.commands[command_name][1])
        self.local_file_counter=0
        for filename in working_dir_list:
            if not self.handle_name_check(filename, old_name):
                continue
            new_name=new_name_rule
            self.working_file=filename
            for to_replace in list(self.renaming_vars.keys()):
                new_name=new_name.replace(to_replace, self.renaming_vars[to_replace]())
            if new_name == filename:
                continue
            if new_name in os.listdir():
                raise ValueError(
                    f'You are trying to rename files ({new_name}) using static name or {new_name} already exists')
            os.rename(filename, new_name)
        return self.commands[command_name][1]

    def delete_files(self, working_dir_list):
        command_name='del'
        file_to_del=self.load_arguments(self.commands[command_name][1])
        if not self.suppresed_question:
            if input(f"You are about to delete files like {file_to_del} in {os.getcwd()}\nTo supress this warning type 'SUP' Press any key to proceed.\n")=='SUP':
                self.suppresed_question=True
        for filename in working_dir_list:
            if not self.handle_name_check(filename, file_to_del):
                continue
            os.remove(os.path.join(os.getcwd(), filename))
        return self.commands[command_name][1]

    def get_working_file_name(self):
        try:
            return self.working_file[:self.working_file.index('.')]
        finally:
            return self.working_file

    @staticmethod
    def get_working_dir(): return os.getcwd().split('\\')[-1]

    def handle_counter(self):
        self.file_counter+=1
        return str(self.file_counter)

    def handle_l_counter(self):
        self.local_file_counter+=1
        return str(self.local_file_counter)

    def handle_reset_counter(self):
        self.file_counter=0

    def handle_end(self):
        self.items_in_loop=[]

    def execute_command_on_stack(self):
        command=self.stack.pop(0)
        if command in self.commands:
            self.commands[command][0]()
        else:
            raise ValueError(f'No function named {command}')

    def load_commands_to_stack(self, list_of_commands):
        if self.stack: raise ValueError('Loaded to many arguments')
        self.stack=list_of_commands
        self.execute_command_on_stack()

    def load_arguments(self, number_of_arguments):
        if len(self.stack) < number_of_arguments: raise ValueError('Function tried to load too many arguments')
        if number_of_arguments==1: return self.stack[0] if self.override_delete_from_stack else self.stack.pop(0)
        to_ret=[]
        for i in range(number_of_arguments):
            to_ret.append(self.stack[i] if self.override_delete_from_stack else self.stack.pop(0))
        return to_ret

    def load_working_dir(self,dirc):
        self.base_working_dir=dirc
        os.chdir(dirc)


base_working_dir=''
answer=input(f'Do you want to work in current dir? ({os.getcwd()})\nY/n: ')
if answer.lower() == 'n':
    while not base_working_dir:
        base_working_dir=input('Directory you want to work in: ')
        if hf.dir_walidate(base_working_dir):
            print(f'Using {base_working_dir}')
        else:
            print('Not viable directory')
            base_working_dir=''
else: base_working_dir=os.getcwd()

interpreter=Interpreter()
interpreter.load_working_dir(base_working_dir)

for line_nr, instruction in enumerate(rs_file):
    instruction_parsed=instruction.split()
    try:
        interpreter.load_commands_to_stack(instruction_parsed)
    except ValueError as encountered_error:
        print(f'{rs_file.name} failed on line {line_nr+1} with error: {encountered_error}')
        input()
print('All files edited successfully!')
input('Press any key to exit...')