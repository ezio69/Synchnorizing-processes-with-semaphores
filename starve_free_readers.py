from threading import Semaphore
import random
import multiprocessing
import time

# initializing
n = 3          # number of writers,readers
critical_section = [0]

nr_active = 0  # number of active readers in critical section
nr_waiting = 0 # number of readers waiting to go into critical section
nw_active = 0  # number of active writers in critical section
nw_waiting = 0 # number of writers waiting to go into critical section

mutex = Semaphore(1)
r_sem = Semaphore(1)
w_sem = Semaphore(1)

def reader(reader_id):
	global nr_active
	global nr_waiting
	global nw_active
	global nw_waiting
	while True:
	    mutex.acquire()
	
	    if nw_active + nw_waiting ==0:
		    nr_active = nr_active + 1   # notify we are active
		    r_sem.release()             # allow ourself to get through
	    else:
		    nr_waiting = nr_waiting + 1 # we are waiting
	    mutex.release()
	    r_sem.acquire()                  # readers will wait here if they must
	    
	    print('reader' + str(reader_id) + ' is reading data...')
	    x = critical_section[0]                         # reading
	    
	    mutex.acquire()
	    nr_active = nr_active - 1
	
	    if nr_active==0 and nw_waiting>0: # if we are the last reader
		
		    while nw_waiting > 0:         # allow all waiting writers to enter
		        w_sem.release()           # wake a writer
		        nw_active = nw_active + 1   # one more active writer
		        nw_waiting = nw_waiting - 1
	    mutex.release()

def writer(writer_id):
	global nr_active
	global nr_waiting
	global nw_active
	global nw_waiting
	while True:
		y = random.randint(1,100)
		mutex.acquire()

		if nr_active + nr_waiting == 0:
			nw_active = nw_active + 1       # notify we are active
			w_sem.release()                 # allow ourself to go through
		else:
			nw_waiting = nw_waiting + 1     # we are waiting
		mutex.release()
		w_sem.acquire()                     # writers will wait here if they must
		print('writer' + str(writer_id) + ' is writing data.....')
		critical_section[0] = y             # writing
		mutex.acquire()
		nw_active = nw_active - 1

		if nw_active ==0 and nr_active>0:   # if we are the last writer
			while nr_waiting > 0:           # allow all waiting readers to enter
				r_sem.release()             # wake a reader
				nr_active = nr_active + 1   # one more active reader
				nr_waiting = nr_waiting - 1
		mutex.release()

process_queue = []

for i in range(0,n):  # n=3 i.e 3 writers and 3 readers
	proc1 = multiprocessing.Process(target=writer,args=(int(i+1),))
	process_queue.append(proc1)
	proc2 = multiprocessing.Process(target=reader,args=(int(i+1),))
	process_queue.append(proc2)

for process in process_queue:
	process.start()

for process in process_queue:
	process.join()