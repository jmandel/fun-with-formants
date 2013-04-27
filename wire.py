"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).
"""

from multiprocessing import Process, Queue
import pyaudio
import struct
import numpy
import plotqueue

CHUNK = 1024
CHANNELS = 1
RATE = 11025
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)

q = Queue()
p = Process(target=plotqueue.f, args=(q,RATE))
p.start()

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")
delay=0
i=0

while True:
    i += 1
    data = stream.read(CHUNK)
    stream.write(data, CHUNK)
    count = len(data)/2 # 2 bytes / sample
    format = "%dh"%(count)
    shorts = numpy.array(struct.unpack( format, data ))
    shorts = shorts * SHORT_NORMALIZE
    q.put(shorts)

print("* done")

stream.stop_stream()
stream.close()

p.terminate()
