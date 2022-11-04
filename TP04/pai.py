import os, time
for i in range(5):
    numFilho = i+1

    pid = os.fork()

    if pid == 0: #filho
        os.execlp("python3", "python3", "filho.py", str(numFilho))
    else:
        print ("PID do filho " + str(numFilho) + " = " + str(pid))