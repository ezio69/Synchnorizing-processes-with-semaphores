from threading import Semaphore
from threading import Lock
import multiprocessing

number_of_philosophers = 5
philosophers = range(0,number_of_philosophers)
state = [2]*number_of_philosophers # Hungry = 0, Eating = 1, Thinking = 2
index = [i for i in range(0,number_of_philosophers-1)] + [-1] # index=[0,1,2,3,-1]

left = []
right = []
for i in index:
    x = philosophers[i-1]
    left.append(x)

for i in index:
    x = philosophers[i+1]
    right.append(x)
  
s= []
for i in range(0,number_of_philosophers):
    x = Semaphore(0)
    s.append(x)

lock = Lock() # mutex lock

def think(i):
    state[i] = 2
    print('philosopher' + str(i+1) +' is thinking....')

def take_chopsticks(i):
    lock.acquire()
    state[i] = 0 # Hungry = 0, Eating = 1, Thinking = 2
    print('philosopher' + str(i+1) + ' is hungry....')
    print('checking if neighbours are eating(using chopsticks)....')
    test(i)
    lock.release()
    s[i].acquire()

def test(i):
    if state[i]==0 and state[left[i]]!=1 and state[right[i]]!=1: # philosopher i can eat only if neither of his neighbours are not eating
        state[i] = 1
        print('philosopher' + str(i+1) is ' takes chopsticks....')
        s[i].release()

def eat(i):
    state[i] = 1
    print('philosopher' + str(i+1) +' starts eating....')

def put_chopsticks(i):
    lock.acquire()
    state[i] = 2 # Hungry = 0, Eating=1, Thinking = 2
    print('philosopher' + str(i+1) +' drops down chopsticks and starts thinking....')
    test(left[i]) # test(left)
    test(right[i]) # test(right)
    lock.release()

def philosopher(i):
    while True:
        think(i)
        take_chopsticks(i)
        eat(i)
        put_chopsticks(i)

process_queue = []

for i in range(0,number_of_philosophers):
    proc = multiprocessing.Process(target=philosopher,args=(int(i),))
    process_queue.append(proc)

for process in process_queue:
    process.start()

for process in process_queue:
    process.join()



