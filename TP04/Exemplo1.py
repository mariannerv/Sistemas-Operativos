import os,time

myVar = 10


def funcao():
    global myVar
    myVar = 1000
    time.sleep(5)

try:
    pid = os.fork()
    if pid == 0: #filho
        funcao()
    else:  #pai
        time.sleep(5)
    print ("Sou o PID = " + str(os.getpid()) + ". myVar = " + str(myVar))

except OSError as e:
    print >>sys.stderr, "fork failed ", e.errno, "-", e.strerror
    sys.exit(1) 