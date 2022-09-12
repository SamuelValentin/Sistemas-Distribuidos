from threading import Thread
import time

check = False
a = False
TIMERCOOR = 15

def func1():
    print("func1 started")
    global a
    while True:
        if check:
            print("got permission")
            a = True
            break
        else:
            time.sleep(0.5)
        

def func2():
    global check
    print ("func2 started")
    time.sleep(1)
    check = True
    time.sleep(1)
    check = False

    print(a)
    print(TIMERCOOR)


if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()