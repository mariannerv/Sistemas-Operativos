import os
import sys
import random
try:
    pid = os.fork()
    if pid == 0: #filho
        x = random.randrange(1,100)
        print ("o filho gerou: "+str(x))
        sys.exit(x)
    else:
        ipid, status = os.wait()
        if os.WIFEXITED(status):
            print ("Valor recebido no processo pai: " +str(os.WEXITSTATUS(status)))
except OSError as e:
    print ("fork failed ", e.errno, "-", e.strerror, file=sys.stderr)
    sys.exit(1)