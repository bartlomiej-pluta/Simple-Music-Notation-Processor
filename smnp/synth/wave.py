import time

import numpy as np
import sounddevice as sd

FS = 44100


def sine(frequency, duration):
    samples = (np.sin(2*np.pi*np.arange(FS*duration)*frequency/FS)).astype(np.float32)
    sd.play(samples, FS)
    time.sleep(duration)