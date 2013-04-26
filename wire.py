"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).
"""

from multiprocessing import Process, Queue
import pyaudio
import struct

import plotqueue

q = Queue()
p = Process(target=plotqueue.f, args=(q,))
p.start()

CHUNK = 256
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")
delay=0
oldbuf = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    count = len(data)/2 # 2 bytes / sample
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    rms = sum([(x*SHORT_NORMALIZE)**2 for x in shorts])**.5 /  count
    q.put(rms)
    oldbuf.append(data)
    if (len(oldbuf) > delay):
        stream.write(oldbuf[i-delay], CHUNK)

print("* done")

stream.stop_stream()
stream.close()

p.terminate()
