from threading import Semaphore
import random
import multiprocessing

num_smokers = 3

mutex = Semaphore(1)
smoker_match = Semaphore(0)
smoker_paper = Semaphore(0)
smoker_tobacco = Semaphore(0)
agent = Semaphore(0) 

def Agent():
	while True:
		mutex.acquire()
		random_num = random.randint(1,3)
		if random_num ==1:
			print('Agent places tobacco and paper on table')
			smoker_match.release()
		elif random_num ==2:
			print('Agent places tobacco and matches on table')
			smoker_paper.release()
		else:
			print('Agent places match and paper on table')
			smoker_tobacco.release()
		mutex.release()
		agent.acquire()

def Smoker(smoker_id):
	while True:
		smoker_tobacco.acquire()
		mutex.acquire()
		print('Smoker' + str(smoker_id) + ' picks up match and paper')
		agent.release()
		mutex.release()
		print('Smoker' + str(smoker_id) + ' smokes')

process_queue = []

proc = multiprocessing.Process(target=Agent)
process_queue.append(proc)

for i in range(0,num_smokers):
	proc = multiprocessing.Process(target=Smoker,args=(int(i+1),))
	process_queue.append(proc)

for process in process_queue:
	process.start()

for process in process_queue:
	process.join()



