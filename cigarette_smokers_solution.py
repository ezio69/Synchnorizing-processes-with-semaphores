import threading
import random

mutex = threading.Semaphore(1)
smoker_match = threading.Semaphore(0)
smoker_paper = threading.Semaphore(0)
smoker_tobacco = threading.Semaphore(0)
agent = threading.Semaphore(0) 

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

def Smoker1():
	while True:
		smoker_match.acquire()
		mutex.acquire()
		print('Smoker1 picks up tobacco and paper')
		agent.release()
		mutex.release()
		print('Smoker1 smokes....')

def Smoker2():
	while True:
		smoker_paper.acquire()
		mutex.acquire()
		print('Smoker2 picks up tobacco and match')
		agent.release()
		mutex.release()
		print('Smoker2 smokes....')

def Smoker3():
	while True:
		smoker_tobacco.acquire()
		mutex.acquire()
		print('Smoker3 picks up match and paper')
		agent.release()
		mutex.release()
		print('Smoker3 smokes....')

agent_thread = threading.Thread(target=Agent)
smoker1_thread = threading.Thread(target=Smoker1)
smoker2_thread = threading.Thread(target=Smoker2)
smoker3_thread = threading.Thread(target=Smoker3)

smoker1_thread.start()
smoker2_thread.start()
agent_thread.start()
smoker3_thread.start()


