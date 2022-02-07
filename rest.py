import psutil
from subprocess import Popen

process_command = ['python3', 'manage.py', 'app']

def restart():
    for process in psutil.process_iter():
        if process.cmdline() == process_command:
            print('Process found. Terminating it.')
            process.terminate()
            break
    print('Process not found: starting it.')
    Popen(process_command)

def stop():
    for process in psutil.process_iter():
        if process.cmdline() == process_command:
            print('Process found. Terminating it.')
            process.terminate()
            break

def print_processes():
    for process in psutil.process_iter():
        print(process.cmdline())

if __name__ == '__main__':
    print_processes()