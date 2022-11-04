import os, time

pid_filho = os.fork()

if pid_filho == 0:
    pid_neto = os.fork()
    
    if pid_neto == 0: 
        print("Eu sou o neto. PID = " + str(os.getpid()))
        time.sleep(5)
    else: #filho
        print("Eu sou o filho. PID = " + str(os.getpid()))
        time.sleep(5)
else: 
    print("Eu sou o pai. PID = " + str(os.getpid()))
    time.sleep(5)
