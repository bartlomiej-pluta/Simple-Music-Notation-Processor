from collections import deque
from statistics import mean

import numpy as np
import sounddevice as sd


class NoiseDetector:
    def __init__(self, noiseTreshold=300, silenceTreshold=10, bufferSize=20):
        self.reachedNoise = False
        self.reachedSilence = False
        self.noiseTreshold = noiseTreshold
        self.silenceTreshold = silenceTreshold
        self.buffer = deque([])
        self.bufferSize = bufferSize    
        self.mean = 0
        
    def callback(self, indata, outdata, frames, time):
        volumeNorm = int(np.linalg.norm(indata)*10)        
        
        if len(self.buffer) < self.bufferSize:
            self.buffer.append(volumeNorm)                
        
        if len(self.buffer) == self.bufferSize:
            self.buffer.rotate(1)
            self.buffer.popleft()            
            self.buffer.appendleft(volumeNorm)     
            self.mean = mean(self.buffer)
            
            if self.mean > self.noiseTreshold:
                self.reachedNoise = True
            if self.reachedNoise and self.mean < self.silenceTreshold:                      
                self.reachedSilence = True            
    
    def waitForComplete(self):        
        with sd.InputStream(callback=self.callback):
            while not self.reachedSilence:
                sd.sleep(10)    
                
    def test(self):
        with sd.InputStream(callback=self.callback):
            while True:
                print(f"Mic level: {self.mean}", end="\r")                 
                sd.sleep(200)                


#TODO: do environment
def waitForSound(args, env):
    noiseTreshold = 300
    silenceTreshold = 10
    if len(args) == 2 and all(isinstance(arg, int) for arg in args):
        noiseTreshold = args[0]
        silenceTreshold = args[1]
    elif len(args) == 1 and isinstance(args[0], int):
        noiseTreshold = args[0]
    elif len(args) > 2:
        return # not valid signature
    detector = NoiseDetector(noiseTreshold, silenceTreshold, 20)
    detector.waitForComplete()
        
