from multiprocessing import Process, Queue

def f(q):
    import matplotlib.pyplot as plt
    import numpy as np
    plt.ion()

    N = 100
    TOP = 0

    values = np.array([0.0] * N)
    l, = plt.plot(range(N), values)

    while True:
        nextval = float(q.get())
        values = np.roll(values, -1)
        values[-1] = nextval
        l.set_ydata(values)
        TOP = max(TOP, max(values))
        print "top", TOP
        plt.ylim([0,TOP])
        plt.draw()

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    while True:
        q.put(raw_input('next val to plot'))
