import os

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_file(interpreter_version):
    file_not_loaded=True
    rs_file=None
    working_dir=os.getcwd()
    print('Trying to locate file...')
    located_rscript_files=[]
    for filename in os.scandir(working_dir):
        if not os.path.isfile(filename):
            continue
        if filename.name.endswith('.rs'):
            located_rscript_files.append(filename.name)

    if located_rscript_files:
        if len(located_rscript_files)>1:
            print(f'Located {len(located_rscript_files)} RenameScript files')
            for inx, name in enumerate(located_rscript_files): print(f'{inx+1}) {name}', end='\n')
            rs_file=open(located_rscript_files[int(input('Choose one by typing number: '))-1])
        else:
            rs_file=open(located_rscript_files[0])
        print(f'Loading file {rs_file.name}...')
    else:
        print(f'{Bcolors.FAIL}Could not locate file automaticly{Bcolors.ENDC}')
        while file_not_loaded:
            try:
                plik=input('RenameScript file path: ')
                rs_file = open(plik)
                print(f'Loading file {rs_file.name}...')
                file_not_loaded=False
            except FileNotFoundError:
                print(f'{Bcolors.FAIL}File not found{Bcolors.ENDC}')
            except:
                raise Exception(f'{Bcolors.FAIL}Unknown file error{Bcolors.ENDC}')

    file_rsversion = rs_file.readline().rstrip()
    if file_rsversion != interpreter_version:
        raise EnvironmentError('Interpreter version and file version do not match up or HEADER is not set up correctly')
    print(f'{Bcolors.OKGREEN}File loaded succesfuly!{Bcolors.ENDC}')
    return rs_file
