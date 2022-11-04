import os, time
from threading import Thread
from multiprocessing import Process

lista = [i for i in range(1,1001)]

t = []


def busca(n_processo, numero):
    for k in range(i*200,200*(n_processo - 1)):
        if lista[k] == numero:
            print("Encontrei o ", numero, "na posição ,", i)
        else:
            print("Não encontrei :(")



for i in range(5):
    t.append(Thread(target= busca, args=(1,5,)))
    t[i].start()


for j in range(5):
    t[j].join()

