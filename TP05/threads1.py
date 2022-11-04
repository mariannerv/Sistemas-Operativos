import time
from threading import Thread
myVar = 10
def funcao():
    global myVar
    myVar = 1000
    print ("Sou a nova thread. myVar= " + str(myVar))
newT = Thread(target = funcao)
newT.start()
newT.join()
print ("Sou a main thread. A nova terminou. myVar = " + str(myVar))

