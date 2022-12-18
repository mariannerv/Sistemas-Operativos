# Grupo: SO-TI-06
# Aluno 1: João Pereira (fc57573)
# Aluno 2: Mariana Valente (fc55945)
# Aluno 3: Tiago Silveira (fc56589)


from asyncore import write
import sys
import os
import re
import signal
import time
import math
import unicodedata
import argparse
from pathlib import Path
import queue
from multiprocessing import Process, Value, Array, Queue, Lock

numberProcess = 0
blockSize=0
counterBlocos=0

linhasC = []
ocorrenciasC = []

linhasPrint = Queue()
linhasTrabalho=0 

parar=Value("i",0)

ficheirosProcessados=Value("i",0)
ficheirosEmProcessamento=Value("i",0)

timerInicial=time.time()

mutexProcessado=Lock()
mutexEmProcessamento=Lock()
mutexLinhas=Lock()
mutexOcorrencias=Lock()
mutexInterromper=Lock()

opcaoLinhas=False
opcaoOcorrencias=False

nL = 0
nO = 0
linhas_imprimirP = []
linhas_imprimirN = ""
paralel=False



# Funções auxiliares


def imprime_linhas(ficheiro, palavra):
    """Verifica quais linhas do ficheiro têm a palavra

    Args:
        ficheiro (file): ficheiro que vai ser analisado
        palavra (str): palavra procurada no ficheiro

    Returns:
        str: linhas no ficheiro que contiam a palavra
    """
    imprimir = ""
    with open(ficheiro, 'r')as f:
        for linha in f:
            if palavra in linha:
                imprimir = imprimir+linha+"\n"
    return imprimir



def conta_ocorrencias(ficheiro, texto):
    """conta as ocorrencias de "texto" no ficheiro e verifica quais linhas do ficheiro têm a palavra

    Args:
        ficheiro (str): ficheiro a ler
        texto (str): string que se pretende contar

    Returns:
       list: [int: numero de ocorrencias da palavra, str: linhas que contêm a palavra]
    """
    imprimir = ""
    counter = 0
    with open(ficheiro) as f:
        for linha in f:
            add = linha.count(texto)
            counter += add
            if texto in linha:
                imprimir = imprimir+linha+"\n"
    return [counter, imprimir]


def conta_linhas_com_palavra(ficheiro, palavra):
    """Conta o numero de linhas em que a palavra aparece (pode aparecer mais do que uma vez) e verifica quais linhas do ficheiro têm a palavra

    Args:
        ficheiro (str): ficheiro a ler
        palavra (str): palavra que se pretende contar
    
    Returns:
        list: [int: numero de linhas com a palavra, str: linhas que contêm a palavra]
    """
    imprimir = ""
    with open(ficheiro) as f:
        count = 0

        lines = f.readlines()
        for line in lines:
            if palavra in line:
                count += 1
                imprimir = imprimir+line+"\n"
        return [count, imprimir]


def conta_linhas_com_palavra_e_ocorrencias(ficheiro, palavra):
    """Conta o numero de linhas com a palavra, o numero de ocorrencias da palavra e verifica as linhas que têm a palavra

    Args:
        ficheiro (file): ficheiro a ler
        palavra (str): palavra a se pesquisar

    Returns:
        list: [int: numero de ocorrencias da palavra, int: numero de linhas com a palavra, str: linhas que contêm a palavra]
    """
    imprimir = ""
    with open(ficheiro) as f:
        countO = 0
        countL = 0
        for linha in f:
            add = linha.count(palavra)
            countO += add
            if palavra in linha:
                countL += 1
                imprimir = imprimir+linha+"\n"
    return [countO, countL, imprimir]


def descobrir_ficheiros_palavra(arg):
    """A partir dos argumentos dados, descobre a palavra e of ficheiros em que serão realizadas as operações

    Args:
        arg (str): argumentos passados

    Returns:
        list: [str: palavra a ser pesquisada, list: Array com os ficheiros a serem utilizados]
    """
    ficheiros = []
    for i in arg:
        if i[0] != "-":
            ficheiros.append(i)
    if "-p" in arg:
        ficheiros = ficheiros[1:]
    if "-e" in arg:
        ficheiros = ficheiros[1:]
    if ficheiros == []:
        return []
    else:
        return [ficheiros[0], ficheiros[1:]]


def separaLinhas(ficheiro):
    """separa as linhas de um ficheiro

    Args:
        ficheiro (file): ficheiro a ser procurado

    Returns:
        list: [str: linhas do ficheiro]
    """
    lista = []
    with open(ficheiro, 'r') as f:
        for linha in f:
            lista.append(linha)
    return lista


def tamanhoFicheirosArray(ficheiros):
    """dado um array de ficheiros, retorna o tamanho total dos seus elementos

    Args:
        ficheiros (list): Array de ficheiros

    Returns:
        int: tamanho total dos ficheiros no array
    """
    total=0
    for ficheiro in ficheiros:
       total+=os.stat(ficheiro).st_size 
    return total

def ficheirosOrdenadosTamanho(ficheiros):
    """Ordenar os ficheiros num array por tamanho

    Args:
        ficheiros (file): Array de ficheiros

    Returns:
        list: [file: ficheiros ordenados por tamanho]
    """
    listaFicheirosOrdenados=[]
    for _ in range(len(ficheiros)):
        ficheiroMaior=""
        fileSize=0
        for ficheiro in ficheiros:
            if (os.stat(ficheiro).st_size >= fileSize) and (ficheiros.count(ficheiro) > listaFicheirosOrdenados.count(ficheiro)):
                ficheiroMaior=ficheiro
                fileSize=os.stat(ficheiro).st_size
        listaFicheirosOrdenados.append(ficheiroMaior)
    return listaFicheirosOrdenados

def auxiliarP(ficheiros, palavra, numberP, lista=[]):
    """Função a ser utilizada pelos processos filhos criados pelo pai quando existe a opcao "-p"

    Args:
        ficheiros (list): Ficheiros a serem analisados pelo processo
        palavra (str): palavra a ser procurada nos ficheiros
        numberP (int): numero do processo
        lista (list, optional): indica as opcoes complementares. Defaults to [].
    """
    imprime = ""
    for i in ficheiros[::-1]:
        mutexInterromper.acquire()
        if parar.value==0:
            mutexInterromper.release()
            mutexEmProcessamento.acquire()
            ficheirosEmProcessamento.value+=1
            mutexEmProcessamento.release()
            if "c" in lista and "l" in lista:
                valores = conta_linhas_com_palavra_e_ocorrencias(i, palavra)
                mutexOcorrencias.acquire()
                ocorrenciasC[numberP] = ocorrenciasC[numberP]+valores[0]
                mutexOcorrencias.release()
                mutexLinhas.acquire()
                linhasC[numberP] = linhasC[numberP]+valores[1]
                mutexLinhas.release()
                imprime = "Ficheiro "+i+":\n"+valores[2]+imprime
            else:
                if "c" in lista:
                    valores = conta_ocorrencias(i, palavra)
                    mutexOcorrencias.acquire()
                    ocorrenciasC[numberP] = ocorrenciasC[numberP]+valores[0]
                    mutexOcorrencias.release()
                    imprime = "Ficheiro "+i+":\n"+valores[1]+imprime
                if "l" in lista:
                    valores = conta_linhas_com_palavra(i, palavra)
                    mutexLinhas.acquire()
                    linhasC[numberP] = linhasC[numberP]+valores[0]
                    mutexLinhas.release()
                    imprime = "Ficheiro "+i+":\n"+valores[1]+imprime
                if lista == []:
                    imprime = "Ficheiro "+i+":\n" + \
                        imprime_linhas(i, palavra)+imprime+"\n"
            mutexProcessado.acquire()
            ficheirosProcessados.value+=1
            mutexProcessado.release()
            mutexEmProcessamento.acquire()
            ficheirosEmProcessamento.value-=1
            mutexEmProcessamento.release()
        else:
            mutexInterromper.release()
            sys.exit("Processo " +str(numberP+1)+ " parou a sua execução!!\n")
    linhasPrint.put("Processo "+str(numberP+1)+":\n"+imprime)


def auxiliarE(palavra, numberP, lista=[]):
    """Função a ser utilizada pelos processos filhos criados pelo pai quando existe a opcao "-e"

    Args:
        palavra (str): palavra a ser procurada nos blocos
        numberP (int): numero do processo
        lista (list, optional): indica as opcoes complementares. Defaults to [].
    """
    i=0
    queueNotEmpty=True
    while(queueNotEmpty):
        try:
            bloco = linhasTrabalho.get(timeout=2.5)
            imprimir=""
            mutexInterromper.acquire()
            if(parar.value==0):
                mutexInterromper.release()
                for i in bloco[0][::-1]:
                    if "c" in lista and "l" in lista:
                        ocorrenciasC[numberP] = ocorrenciasC[numberP]+i.count(palavra)
                        if palavra in i:
                            linhasC[numberP] = linhasC[numberP]+1
                            imprimir = i+imprimir
                    else:
                        if "c" in lista:
                            ocorrenciasC[numberP] = ocorrenciasC[numberP] + i.count(palavra)
                            if palavra in i:
                                imprimir = i+imprimir
                        elif "l" in lista:
                            if palavra in i:
                                linhasC[numberP] = linhasC[numberP]+1
                                imprimir = i+imprimir
                        else:
                            if palavra in i:
                                imprimir = i+imprimir
                linhasPrint.put("Ficheiro "+bloco[1]+":\n"+imprimir)
            else:
                mutexInterromper.release()
                sys.exit("Processo " +str(numberP+1)+ " parou a sua execução!!\n")
        except queue.Empty:
            queueNotEmpty=False
    sys.exit()


def processosP(n, ficheiros, palavra, lista=[]):
    """Função auxiliar para criar processos filhos e lhes atribuir ficheiros

    Args:
        n (int): numero de processos
        ficheiros (Arr): ficheiros a serem procurados pelos filhos
        palavra (str): palavra a ser procurada nos ficheiros
        lista (list, optional): indica as opcoes complementares. Defaults to [].
    """
    if n > len(ficheiros):
        n = len(ficheiros)
    listaProcessos = []
    listaFicheirosOrdenados=ficheirosOrdenadosTamanho(ficheiros)
    listaFicheirosPorProcessos=[]
    for _ in range(n):
        listaFicheirosPorProcessos.append([])
    for item in listaFicheirosOrdenados:
        sumProcesso=tamanhoFicheirosArray(listaFicheirosPorProcessos[0])
        indLocation=0
        for ite in range(len(listaFicheirosPorProcessos)):
            if tamanhoFicheirosArray(listaFicheirosPorProcessos[ite])<sumProcesso:
                sumProcesso=tamanhoFicheirosArray(listaFicheirosPorProcessos[ite])
                indLocation=ite
        listaFicheirosPorProcessos[indLocation].append(item)

    for i in range(n):
        listaProcessos.append(Process(target=auxiliarP, args=(listaFicheirosPorProcessos[i], palavra, i, lista,)))
        listaProcessos[i].start()

    for k in listaProcessos:
        k.join()

def processosE(n, ficheiros, palavra, lista=[]):
    """Função auxiliar para criar processos filhos e fazer a criação dos blocos que serão atribuidos aos filhos

    Args:
        n (int): numero de processos
        ficheiros (Arr): ficheiros a serem procurados pelos filhos
        palavra (str): palavra a ser procurada nos blocos
        lista (list, optional): indica as opcoes complementares. Defaults to [].
    """
    global counterBlocos
    listaProcessos = []
    for i in range(n):
        listaProcessos.append(Process(target=auxiliarE, args=(palavra, i, lista,)))
        listaProcessos[i].start()
    for ficheiro in ficheiros:
        mutexEmProcessamento.acquire()
        ficheirosEmProcessamento.value+=1
        mutexEmProcessamento.release()
        blocoP=[]
        blocoF=""
        with open(ficheiro,"r") as f:
            linhas=f.readlines()
            for linha in linhas:
                blocoF+=linha
                if sys.getsizeof(blocoF) > blockSize:
                    linhasTrabalho.put([blocoP,ficheiro],block=True)
                    counterBlocos+=1
                    blocoP=[]
                    blocoF=""
                    blocoF+=linha
                    blocoP.append(linha)
                elif sys.getsizeof(blocoF) == blockSize:
                    blocoP.append(linha)
                    linhasTrabalho.put([blocoP,ficheiro],block=True)
                    counterBlocos+=1
                    blocoP=[]
                    blocoF=""
                elif sys.getsizeof(blocoF) < blockSize:
                    blocoP.append(linha)
            linhasTrabalho.put([blocoP,ficheiro],block=True)
            counterBlocos+=1
        mutexEmProcessamento.acquire()
        ficheirosEmProcessamento.value-=1
        mutexEmProcessamento.release()
        mutexProcessado.acquire()
        ficheirosProcessados.value+=1
        mutexProcessado.release()


    for k in listaProcessos:
        k.join()



# Função principal a ser executada

def main(args):
    print('Programa: pgrepwc_processos.py')
    print('Argumentos: ', args)
    buscas = descobrir_ficheiros_palavra(args)

    global numberProcess
    global counterBlocos
    global nL 
    global nO 
    global linhas_imprimirP
    global linhas_imprimirN 
    global paralel
    # Caso o utilizador não introduza uma palavra
    if buscas == []:
        print("Não introduziu qualquer palavra para ser pesquisada")
        return
    # Caso o ututilizador não introduza ficheiro, pedir o nome de um ficheiro ao utilizador
    while buscas[1] == []:
        ficheiro = input("Insira o nome do ficheiro: ")
        buscas[1] = [ficheiro]
    # Verificação dos diferentes casos
    if "-p" in args or "-e" in args:
        casos = []
        paralel=True
        if "-c" in args:
            casos.append("c")
        if "-l" in args:
            casos.append("l")
        if "-e" in args and "-p" in args:
                processosE(numberProcess, buscas[1], buscas[0], casos)
                mutexInterromper.acquire()
                if(parar.value==0):
                    printOrganizar=""
                    for i in range(counterBlocos):
                        linhas_imprimirP.append(linhasPrint.get())
                    for b in buscas[1]:
                        printOrganizar+="\n"+b+": \n\n"
                        for l in linhas_imprimirP:
                            if (b in l):
                                printOrganizar+=l[11+len(b):]
                    print(printOrganizar)
                mutexInterromper.release()
                if "-c" in args:
                    print("O numero total de vezes no qual a palavra ocorreu é:", sum(
                        ocorrenciasC))
                if "-l" in args:
                    print(
                        "O numero total de linhas no qual a palavra ocorreu é:", sum(linhasC))
                return
        else:
            processosP(numberProcess, buscas[1], buscas[0], casos)
            mutexInterromper.acquire()
            if(parar.value==0):
                mutexInterromper.release()
                if numberProcess > len(buscas[1]):
                    numberProcess = len(buscas[1])
                for i in range(numberProcess):
                    linhas_imprimirP.append(linhasPrint.get())
                for p in range(len(linhas_imprimirP)):
                    for l in linhas_imprimirP:
                        if int(l[9]) == (p+1):
                            print(l)
            if "-c" in args:
                print("O numero total de vezes no qual a palavra ocorreu é:", sum(
                    ocorrenciasC))
            if "-l" in args:
                print(
                    "O numero total de linhas no qual a palavra ocorreu é:", sum(linhasC))
    else:
        for i in buscas[1][::-1]:
            mutexInterromper.acquire()
            a=parar.value
            mutexInterromper.release()
            if parar.value==0:
                mutexEmProcessamento.acquire()
                ficheirosEmProcessamento.value+=1
                mutexEmProcessamento.release()
                if "-c" in args and "-l" in args:
                    valores = conta_linhas_com_palavra_e_ocorrencias(i, buscas[0])
                    mutexOcorrencias.acquire()
                    nO = nO+valores[0]
                    mutexOcorrencias.release()
                    mutexLinhas.acquire()
                    nL = nL+valores[1]
                    mutexLinhas.release()
                    linhas_imprimirN = "Ficheiro "+i + \
                        ":\n"+valores[2]+linhas_imprimirN
                else:
                    if "-c" in args:
                        valores = conta_ocorrencias(i, buscas[0])
                        mutexOcorrencias.acquire()
                        nO = nO+valores[0]
                        mutexOcorrencias.release()
                        linhas_imprimirN = "Ficheiro "+i + \
                            ":\n"+valores[1]+linhas_imprimirN
                    elif "-l" in args:
                        valores = conta_linhas_com_palavra(i, buscas[0])
                        mutexLinhas.acquire()
                        nL = nL+valores[0]
                        mutexLinhas.release()
                        linhas_imprimirN = "Ficheiro "+i + \
                            ":\n"+valores[1]+linhas_imprimirN
                    else:
                        # Imprimir as linhas que contem a palavra escolhida pelo utilizador
                        linhas_imprimirN = "Ficheiro "+i+":\n" + \
                            imprime_linhas(i, buscas[0])+linhas_imprimirN
                mutexProcessado.acquire()           
                ficheirosProcessados.value+=1
                mutexProcessado.release()
                mutexEmProcessamento.acquire()
                ficheirosEmProcessamento.value-=1
                mutexEmProcessamento.release() 
        mutexInterromper.acquire()
        if(parar.value==0):
            print(linhas_imprimirN)
        mutexInterromper.release()
        if "-c" in args:
            print("O numero total de vezes no qual a palavra ocorreu é:", nO)
        if "-l" in args:
            print("O numero total de linhas no qual a palavra ocorreu é:", nL)


def controlC(sig, NULL):
    """Interromper os processoas apos terminarem os ficheiros currents

    Args:
    """
    mutexInterromper.acquire()
    if(parar.value==0):
        parar.value=1
        print("\nFoi sinalizada a interrupção, a terminar ficheiros atuais!\n")
    mutexInterromper.release()

signal.signal(signal.SIGINT, controlC)

def resultadosParciais(sig, NULL):
    """Alarme para imprimir resultados parciais

    Args:
    """
    global paralel
    global nL
    global nO
    if paralel==True:
        if (opcaoLinhas):
            mutexLinhas.acquire()
            print("Numero de ocorrencias da palavra em linhas: "+str(sum(linhasC)))
            mutexLinhas.release()
        if(opcaoOcorrencias):
            mutexOcorrencias.acquire()
            print("Numero de ocorrencias da palavra: "+str(sum(ocorrenciasC)))
            mutexOcorrencias.release()
        mutexProcessado.acquire()
        print("Numero de ficheiros ja processados: "+str(ficheirosProcessados.value))
        mutexProcessado.release()
        mutexEmProcessamento.acquire()
        print("Numero de ficheiros em processamento: "+str(ficheirosEmProcessamento.value))
        mutexEmProcessamento.release()
        print("Desde o inicio da analise dos ficheiros, passaram: "+str(round((time.time()-timerInicial)*1000000))+" microsegundos.\n")
    else:
        if(opcaoLinhas):
            mutexLinhas.acquire()
            print("Numero de ocorrencias da palavra em linhas: "+str(nL))
            mutexLinhas.release()
        if(opcaoOcorrencias):
            mutexOcorrencias.acquire()
            print("Numero de ocorrencias da palavra: "+str(nO))
            mutexOcorrencias.release()
        mutexProcessado.acquire()
        print("Numero de ficheiros ja processados: "+str(ficheirosProcessados.value))
        mutexProcessado.release()
        mutexEmProcessamento.acquire()
        print("Numero de ficheiros em processamento: "+str(ficheirosEmProcessamento.value))
        mutexEmProcessamento.release()
        print("Desde o inicio da analise dos ficheiros, passaram: "+str(round((time.time()-timerInicial)*1000000))+" microsegundos.\n")


signal.signal(signal.SIGALRM, resultadosParciais)
signal.setitimer(signal.ITIMER_REAL, 3, 3)  

if __name__ == "__main__":
    numberL = []
    if "-p" in sys.argv:
        for i in sys.argv[1:]:
            if i[0] != "-":
                numberL.append(i)
        numberProcess = int(numberL[0])
        if"-e" in sys.argv:
            blockSize=int(numberL[1])
            linhasTrabalho=Queue(maxsize=math.ceil(1048576/blockSize))
    if "-c" in sys.argv:
        opcaoOcorrencias=True
    if "-l" in sys.argv:
        opcaoLinhas=True
    linhasC = Array("i", numberProcess)
    ocorrenciasC = Array("i", numberProcess)
    main(sys.argv[1:])


timerInicial=time.time()