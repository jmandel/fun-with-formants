from multiprocessing import Process, Queue
import time

def f(q):
    import matplotlib.pyplot as plt
    import numpy as np
    plt.ion()

    N = 100
    values = np.array([0.0] * N)
    l, = plt.plot(range(N), values)
    plt.ylim([0,1])

    while True:
        news = []
        while True:
            try: 
                news.append(float(q.get()))
            except Queue.Empty:
                break

        values = np.roll(values, -1 * len(news))
        values[-1*len(news):] = news
        print values[-1*len(news):]
        l.set_ydata(values)
        plt.draw()

        time.sleep(0.1)

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    while True:
        q.put(raw_input('next val to plot'))
