import os, time
from threading import Thread
from multiprocessing import Process

sum=0
def calc_sum(num):
    global sum
    for i in range(num+1):
        sum += i
    print ("soma na funcao: ", str(sum))


newT = Thread(target = calc_sum, args = (15,))
newT.start()
newT.join()

print("Sou a main thread. A nova terminou. Soma = " + str(sum))