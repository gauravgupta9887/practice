import threading
import time


def func1():
    for i in range(3):
        time.sleep(1)
        print("Inside func 1")


def func2():
    for i in range(5):
        time.sleep(.8)
        print("Inside func 2")


threading.Thread(target=func1).start()
threading.Thread(target=func2).start()

print("Threads started")
