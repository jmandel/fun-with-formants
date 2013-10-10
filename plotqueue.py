from multiprocessing import Process, Queue
import Queue as EQ
import time

def f(q, RATE):
    import matplotlib.pyplot as plt
    import numpy as np
    import lpc
    import math
    from scipy.signal import lfilter
    plt.ion()

    N = 100
    TOP = 0

    values = np.array([0.0] * N)
    print "looping"
    l = None
    shorts = None
    while True:
        qs = q.qsize()
        # if qs>0:
        #     print "q @ ", qs
        try:
            newshorts = q.get_nowait()
            shorts = newshorts
            #print "drain"
        except EQ.Empty:
            if (shorts != None):
                """
                ac= np.correlate(shorts, shorts, mode='full')
                ac = ac[len(ac)/2:]
                peaks = (np.diff(np.sign(np.diff(ac))) < 0).nonzero()[0] + 1
                peaks_hz = [RATE/x for x in peaks[:3]]
                pstr= ", ".join(["%s hz"%(RATE / x) for x in peaks[:3]])
                plt.title(pstr, fontsize=14, fontweight='bold')
                """

                shorts = shorts * np.hamming(len(shorts))
                shorts = lfilter([1], [1, .63], shorts)
                A = lpc.lpc_ref(shorts, 9)
                roots = np.roots(A)
                roots = roots[np.imag(roots)<0]
                bw= -.5 * RATE / 2 / math.pi * np.log(np.abs(roots))
                angs = np.arctan2(np.imag(roots), np.real(roots))
                angs = angs * [RATE / 2 / math.pi]
                angs = np.absolute(angs)
                order = np.argsort(angs)
                #for v in  zip(angs, bw): print v
                #print "\n\n***"
                tstr= "    ".join(["{0:10d} hz".format(int(angs[order[i]])) for i in range(len(order)) if bw[order[i]] < 400])


                plt.title(tstr, fontsize=14, fontweight='bold')

                #print "lpc", A



                fft = np.fft.rfft(shorts)
                afft = np.absolute(fft)
                #sizeprint np.arange(len(fft)), np.absolute(fft)
                plt.clf()
                plt.xlim([0,3000])
                plt.ylim([0, 3000])
                print len(angs)
                print [angs[order[i]] for i in range(len(order))]
                h=plt.plot(angs[order[1]], angs[order[2]], 'ro')
                if np.mean(shorts**2) > 10e-8:
                    plt.draw()

                #rms = sum([x**2 for x in shorts])**.5 /  len(shorts)
                #news.append(rms)
    if len(news) > 0 and False:
            values = np.roll(values, -1 * len(news))
            values[-1*len(news):] = news
            l.set_ydata(values)
            TOP = max(TOP, max(values))
            plt.ylim([0,TOP])
            plt.draw()

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    while True:
        q.put(raw_input('next val to plot'))
