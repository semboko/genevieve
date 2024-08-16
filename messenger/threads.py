from threading import Thread


def thread1():
    for _ in range(100):
        print("Hello from thread 1")


def thread2():
    for _ in range(100):
        print("Hello from thread 2")


t1 = Thread(target=thread1)
t2 = Thread(target=thread2)

t1.start()
t2.start()
