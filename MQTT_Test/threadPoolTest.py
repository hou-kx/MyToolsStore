from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time


# 定义一个准备作为线程任务的函数
def hello(n):
    for _ in range(n):
        time.sleep(1)
        print('Hello World:%s' % time.time())
    pass


def ceshi():
    while True:
        i = input()
        print("send: ", i)
        if i == '$':
            break


pool = ThreadPoolExecutor(max_workers=2)  # 创建一个包含2条线程的线程池

future1 = pool.submit(hello, 10)  # 向线程池提交一个task, 50会作为action()函数的参数
future2 = pool.submit(ceshi)  # 向线程池再提交一个task, 100会作为action()函数的参数
as_completed([future2])
pool.shutdown()  # 关闭线程池
