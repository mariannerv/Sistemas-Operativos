# Grupo: SO-TI-06
# Aluno 1: João Pereira (fc57573)
# Aluno 2: Mariana Valente (fc55945)
# Aluno 3: Tiago Silveira (fc56589)


from asyncore import write
import sys
import os
import re
import unicodedata
import argparse
from threading import Thread

numberThread = 0

linhasC = []
ocorrenciasC = []
linhasImprime = []


# retorna as linhas de um ficheiro que contêm a palavra
def imprime_linhas(ficheiro, palavra):
    imprimir = ""
    with open(ficheiro, 'r')as f:
        for linha in f:
            if palavra in linha:
                imprimir = imprimir+linha+"\n"
    return imprimir


# retorna o numero de ocorrencias de uma palavra num ficheiro, e retorna as linhas que as contêm
def conta_ocorrencias(ficheiro, texto):
    """conta as ocorrencias de "texto" no ficheiro

    Args:
        ficheiro (str): ficheiro a ler
        texto (str): string que se pretende contar

    Returns:
       int: numero de ocorrencias do texto no ficheiro
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


# retorna o numero de linhas que contêm a palavra e as linhas
def conta_linhas_com_palavra(ficheiro, palavra):
    """Conta o numero de linhas em que a palavra aparece (pode aparecer mais do que uma vez)

    Args:
        ficheiro (str): ficheiro a ler
        palavra (str): palavra que se pretende contar
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


# retorna o numero de ocorrências individuais da palavra, o numero de linhas que contêm essa palavra e as linhas
def conta_linhas_com_palavra_e_ocorrencias(ficheiro, palavra):
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


# retorna uma lista, cujo primeiro elemento é a palavra a ser pesquisada, e cujos outros elementos são os ficheiros no qual a palavra sera pesquisada
def descobrir_ficheiros_palavra(arg):
    ficheiros = []
    for i in arg:
        if i[0] != "-":
            ficheiros.append(i)
    if "-p" in arg:
        ficheiros = ficheiros[1:]
    if ficheiros == []:
        return []
    else:
        return [ficheiros[0], ficheiros[1:]]


# retorna um array, sendo cada elemento do array uma linha de texto de um ficheiro
def separaLinhas(ficheiro):
    lista = []
    with open(ficheiro, 'r') as f:
        for linha in f:
            lista.append(linha)
    return lista


# Auxilia a realização da opção -p, realizando os diferentes casos dependendo das outras opções("-c" e "-l")
def auxiliarP(ficheiros, palavra, numberT, lista=[]):
    global ocorrenciasC
    global linhasC

    imprimir_linhas = ""

    for i in ficheiros[::-1]:
        if "c" in lista and "l" in lista:
            valores = conta_linhas_com_palavra_e_ocorrencias(i, palavra)
            ocorrenciasC[numberT] = ocorrenciasC[numberT]+valores[0]
            linhasC[numberT] = linhasC[numberT]+valores[1]
            imprimir_linhas = "Ficheiro "+i+":\n"+valores[2]+imprimir_linhas
        else:
            if "c" in lista:
                valores = conta_ocorrencias(i, palavra)
                ocorrenciasC[numberT] = ocorrenciasC[numberT]+valores[0]
                imprimir_linhas = "Ficheiro "+i + \
                    ":\n"+valores[1]+imprimir_linhas
            elif "l" in lista:
                valores = conta_linhas_com_palavra(i, palavra)
                linhasC[numberT] = linhasC[numberT]+valores[0]
                imprimir_linhas = "Ficheiro "+i + \
                    ":\n"+valores[1]+imprimir_linhas
            else:
                imprimir_linhas = "Ficheiro "+i+":\n" + \
                    imprime_linhas(i, palavra)+imprimir_linhas
    linhasImprime[numberT] = "Thread "+str(numberT+1)+":\n"+imprimir_linhas

# Auxilia a realização da opção -e, realizando os diferentes casos dependendo das outras opções("-c" e "-l")


def auxiliarE(linhas, palavra, numberT, lista=[]):
    global ocorrenciasC
    global linhasC

    imprimir_linhas = ""

    for i in linhas[::-1]:
        if "c" in lista and "l" in lista:
            ocorrenciasC[numberT] = ocorrenciasC[numberT]+i.count(palavra)
            if palavra in i:
                linhasC[numberT] = linhasC[numberT]+1
                imprimir_linhas = i+imprimir_linhas
        else:
            if "c" in lista:
                ocorrenciasC[numberT] = ocorrenciasC[numberT] + \
                    i.count(palavra)
                if palavra in i:
                    imprimir_linhas = i+imprimir_linhas
            elif "l" in lista:
                if palavra in i:
                    linhasC[numberT] = linhasC[numberT]+1
                    imprimir_linhas = i+imprimir_linhas
            else:
                if palavra in i:
                    imprimir_linhas = i+imprimir_linhas
    imprimir_linhas = imprimir_linhas+"\n"
    linhasImprime[numberT] = "Thread "+str(numberT+1)+":\n"+imprimir_linhas


# realiza a distribuição da pesquisa, com a opção -p, sobre os ficheiros pelo dado numero de processos
def threadsP(n, ficheiros, palavra, lista=[]):
    if n > len(ficheiros):
        n = len(ficheiros)
    listaProcessos = []
    for i in range(n):
        j = Thread(target=auxiliarP, args=(ficheiros[round(
            len(ficheiros)/n*i):round(len(ficheiros)/n*(i+1))], palavra, i, lista,))
        j.start()
        listaProcessos.append(j)
    for k in listaProcessos:
        k.join()


# realiza a distribuição da pesquisa, com a opção -e, sobre os ficheiros pelo dado numero de processos
def threadsE(n, ficheiro, palavra, lista=[]):
    separada = separaLinhas(ficheiro)
    listaProcessos = []
    for i in range(n):
        j = Thread(target=auxiliarE, args=(separada[round(
            len(separada)/n*i):round(len(separada)/n*(i+1))], palavra, i, lista,))
        j.start()
        listaProcessos.append(j)
    for k in listaProcessos:
        k.join()


# Função principal a ser executada
def main(args):
    print('Programa: pgrepwc_threads.py')
    print('Argumentos: ', args)
    buscas = descobrir_ficheiros_palavra(args)

    global ocorrenciasC
    global linhasC
    global numberThread
    global linhasImprime

    linhas_imprimir = ""
    nO = 0
    nL = 0

    # Caso o utilizador não introduza uma palavra
    if buscas == []:
        print("Não introduziu qualquer palavra para ser pesquisada")
        return
    # Caso o ututilizador não introduza ficheiro, pedir o nome de um ficheiro ao utilizador
    if buscas[1] == []:
        ficheiro = input("Insira o nome do ficheiro: ")
        buscas[1] = [ficheiro]
    # Verificação dos diferentes casos
    if "-p" in args or "-e" in args:
        casos = []
        if "-c" in args:
            casos.append("c")
        if "-l" in args:
            casos.append("l")
        if "-e" in args and "-p" in args:
            if len(buscas[1]) == 1:
                threadsE(numberThread, buscas[1][0], buscas[0], casos)
                for p in range(len(linhasImprime)):
                    for l in linhasImprime:
                        if l != 0:
                            if int(l[7]) == (p+1):
                                print(l)
            else:
                print(
                    "Só pode dar um ficheiro para ser analisado quando ativada a opção -e")
        else:
            threadsP(numberThread, buscas[1], buscas[0], casos)
            for p in range(len(linhasImprime)):
                for l in linhasImprime:
                    if l != 0:
                        if int(l[7]) == (p+1):
                            print(l)
        if "-c" in args:
            print("O numero total de vezes no qual a palavra ocorreu é:",
                  sum(ocorrenciasC))
        if "-l" in args:
            print("O numero total de linhas no qual a palavra ocorreu é:", sum(linhasC))
    else:
        for i in buscas[1][::-1]:
            if "-c" in args and "-l" in args:
                valores = conta_linhas_com_palavra_e_ocorrencias(i, buscas[0])
                nO = nO+valores[0]
                nL = nL+valores[1]
                linhas_imprimir = "Ficheiro "+i + \
                    ":\n"+valores[2]+linhas_imprimir
            else:
                if "-c" in args:
                    valores = conta_ocorrencias(i, buscas[0])
                    nO = nO+valores[0]
                    linhas_imprimir = "Ficheiro "+i + \
                        ":\n"+valores[1]+linhas_imprimir
                elif "-l" in args:
                    valores = conta_linhas_com_palavra(i, buscas[0])
                    nL = nL+valores[0]
                    linhas_imprimir = "Ficheiro "+i + \
                        ":\n"+valores[1]+linhas_imprimir
                else:
                    # Imprimir as linhas que contem a palavra escolhida pelo utilizador
                    linhas_imprimir = "Ficheiro "+i+":\n" + \
                        imprime_linhas(i, buscas[0])+linhas_imprimir
        print(linhas_imprimir)
        if "-c" in args:
            print("O numero total de vezes no qual a palavra ocorreu é:", nO)
        if "-l" in args:
            print("O numero total de linhas no qual a palavra ocorreu é:", nL)


if __name__ == "__main__":
    numberL = []
    if "-p" in sys.argv:
        for i in sys.argv[1:]:
            if i[0] != "-":
                numberL.append(i)
        numberThread = int(numberL[0])
    for i in range(numberThread):
        linhasC.append(0)
        ocorrenciasC.append(0)
        linhasImprime.append(0)
    main(sys.argv[1:])
