import os, sys
try:
    os.fork()
    os.fork()
    os.fork()
    file=open("TMP"+str(os.getpid()),'w')
    file.close()
except OSError as e:
    print ("fork failed ", e.errno, "-", e.strerror, file=sys.stderr)
    sys.exit(1) 