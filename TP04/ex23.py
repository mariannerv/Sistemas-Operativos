import os, sys
try:
    n = 1
    if os.fork() == 0:
        if os.fork() == 0:
            if os.fork() == 0:
                pass #do nothing
            else: 
                n += 1
        else:
            n += 2    
            if os.fork() == 0:
            else: 
                pass
    else:
        if os.fork() == 0:
        else:
            pass

        
    os.fork()
    os.fork()
    file=open("TMP"+str(os.getpid()),'w')
    file.close()
except OSError as e:
    print ("fork failed ", e.errno, "-", e.strerror, file=sys.stderr)
    sys.exit(1) 