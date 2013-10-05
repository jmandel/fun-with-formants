import numpy as np
import pymc as mc
from pylab import hist, show, figure

chunks = [
  {
    'target': 5,
    'ear':   [5,6,4,5,5,4,5,5,5],
    'mouth': [5,6,4,5,5,4,5,5,5]
  }, {
    'target': 5,
    'ear':   [4.9,4.7,3.6,3,3.1,4.1,5.1,3.1,1.1],
    'mouth': [4.1,4.1,3.1,4.1,4.1,3.1,4.1,4.1,4.1]
  }, {
    'target': 5,
    'ear':   [5,5,5,5,5,6,4,5,5],
    'mouth': [5,5,5,5,5,6,4,5,5]
  },
]

mouthFactor =  [
  mc.Uniform('mouthFactor%s'%i, 0, 1, value=0) 
  for i in range(len(chunks)-1)
]

def gap(n):
    chunkMouth = chunks[n]['mouth']
    chunkEar = chunks[n]['ear']
    target = chunks[n]['target']
    def gapfunc(mouthFactor):
        ret = []
        for v in range(len(chunkMouth)):
            gap = 0
            gap += (target - chunkMouth[v])*mouthFactor
            gap += (target - chunkEar[v])*(1-mouthFactor)
            ret.append(gap)
        return ret
    return gapfunc

gaps = [
    mc.Deterministic(eval = gap(i),
                  name = 'gap%s'%i,
                  parents = {'mouthFactor': mouthFactor[i]},
                  doc='gap %s'%i)
    for i in range(len(chunks)-1)
]

def chunkPrediction(n):
    chunk = chunks[n]['mouth']
    def predict(gap):
        ret = []
        for v in range(len(gap)):
            ret.append(chunk[v] + gap[v])
        return ret
    return predict

predictions = [
    mc.Deterministic(eval = chunkPrediction(i),
                      name = 'chunk%sPrediction'%i,
                      parents = {'gap': gaps[i]},
                      doc='chunk %s prediction'%i)
    for i in range(len(chunks)-1)
]

noise=mc.Exponential('noise', 1,1)

observations = [
    mc.Normal('chunk%sObservation'%i, predictions[i-1], noise, value=chunks[i-1]['mouth'], observed=True)
    for i in range(1,len(chunks))
]

@mc.deterministic
def mouthChanges(early=mouthFactor[0], late=mouthFactor[1]):
 return late-early

S = mc.MCMC([noise, mouthChanges, mouthFactor])
S.sample(500000, burn=1000)
hist(S.trace('mouthFactor0')[:], 50, color='b', alpha=.4)
hist(S.trace('mouthFactor1')[:], 50, color='r', alpha=.4)
figure()

delta_samples=S.trace('mouthChanges')[:]

hist(delta_samples, 50, color='y', alpha=.4)

print "Probability mouth sensitivity INCREASES over time: %.3f" % \
    (delta_samples > 0).mean()
    
figure()

hist(S.trace('noise')[:], 50, color='g', alpha=.4)
