from multiprocessing import Process, Array, Semaphore
import random, time

MAX_SIZE = 5
buffer = Array("i",MAX_SIZE)
empty = Semaphore(MAX_SIZE) #Inicialmente, MAX_SIZE posicoes livres
full = Semaphore(0)         #Inicialmente, 0 posicoes ocupadas
mutex_1 = Semaphore(1)
mutex_2 = Semaphore(1)

def produtor():
	inPosition =0
	while True:
		nextProduced = random.randint(1,100)
		empty.acquire() #Ha’ posicoes livres?
		buffer[inPosition] = nextProduced
		temp = inPosition
		mutex_1.acquire()
		inPosition = (inPosition + 1) % MAX_SIZE
		mutex_1.release()
		full.release() #Informo que há nova posicao ocupada
		print ("+++Produzi ") + str(nextProduced) + " na posicao " + str(temp)
		time.sleep(random.randint(0,3)) #descanso um pouco

def consumidor():
	outPosition = 0
	while True:
		full.acquire()
		nextConsumed = buffer[outPosition]
		temp_2=outPosition
		mutex_2.acquire()
		outPosition = (outPosition + 1) % MAX_SIZE
		mutex_2.release()
		empty.release()
		print ("+++Comsumi ") + str(nextConsumed) + " na posicao " + str(temp_2)
		time.sleep(random.randint(0,3)) #descanso um pouco

prod = Process(target=produtor)
cons = Process(target=consumidor)
prod1 = Process(target=produtor)
cons1 = Process(target=consumidor)

prod.start()
cons.start()
prod1.start()
cons1.start()

prod.join()
cons.join()
prod1.join()
cons1.join()