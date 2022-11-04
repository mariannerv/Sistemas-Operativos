import os, sys
n=10
try:
    pid = os.fork()
    if pid == 0: #filho
        print("hello, n=", n/2)
    else: #pai
        print("hello, n=", n*2)
except OSError as e:
    print(sys.stderr, "fork failed ", e.errno, "-", e.strerror)
    sys.exit(1) 
