from threading import Semaphore
from threading import Thread
import time

n = 10

barber_sleeping = Semaphore(1)
customers_waiting =[0]*n 
in_chair = Semaphore(0)
cut_done =  Semaphore(n)

mutex = Semaphore(1)

def compute_customers_waiting(customers_waiting):
	total_customers_waiting = 0
	for customer_waiting in customers_waiting:
		if customer_waiting == 1:
			total_customers_waiting+=1
	return total_customers_waiting

def get_hair_cut(j):
	customers_waiting[j] = 1
	
def give_hair_cut():
	print('Haircut done!')

def Barber():
	i=0
	while True:
	    mutex.acquire()
	    if compute_customers_waiting(customers_waiting) == 0:
		    mutex.release()
		    print('barber sleeping.......')
		    barber_sleeping.acquire()
		    mutex.acquire()
	    mutex.release()
	    customers_waiting[i] = 0
	    print('Haircut started')
	    in_chair.release()
	    give_hair_cut()
	    cut_done.release()
	    i = (i+1) % n
	    time.sleep(0.25)

def Customer():
	j = 0
	while True:
		mutex.acquire()
		if compute_customers_waiting(customers_waiting) == n:
			mutex.release()
			print('Customer leaves as shop is full!')
		else:
			customers_waiting[j] = 1
			print('New Customer enters shop')
			if customers_waiting ==1:
				barber_sleeping.release()
			mutex.release()
			in_chair.acquire()
			get_hair_cut(j)
			cut_done.acquire()
			j = (j+1) % n
			time.sleep(0.25)

barber_thread = Thread(target=Barber)
customer_thread = Thread(target=Customer)

barber_thread.start()
customer_thread.start()


