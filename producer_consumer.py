import threading
import random
import time

# initializing buffers
print('Initializing buffer....')
buffer_size = 10
buffer = [0]*buffer_size
print(buffer)

# creating and initializing semaphores
full = threading.Semaphore(0)
empty = threading.Semaphore(buffer_size)

def insert_item(buffer,i,x):
	buffer[i] = x
	print(buffer)

def remove_item(buffer,j):
	buffer[j] = 0
	print(buffer)

def producer():
    i = 0
    while True:
        x = random.randint(1,100) # random number between 1 and 100
        empty.acquire()
        insert_item(buffer,i,x)
        full.release()
        i = (i + 1) % buffer_size
        time.sleep(0.25) # sleep the thread for 0.25s to see both insert and remove changes take place

def consumer():
    j = 0
    while True:
        full.acquire()
        y = buffer[j]
        empty.release()
        remove_item(buffer,j)
        j = (j + 1) % buffer_size
        time.sleep(0.25)

producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()
