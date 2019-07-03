from smnp.note.pitch import NotePitch

semitonesToIntervalName = {
        0: "1",
        1: "2m",
        2: "2M",
        3: "3m",
        4: "3M",
        5: "4",
        6: "5d/4A",
        7: "5",
        8: "6m",
        9: "6M",
        10: "7m",
        11: "7M"        
    }

def intervalToString(interval):
    octaveInterval = int(abs(interval) / len(NotePitch))
    pitchInterval = abs(interval) % len(NotePitch)
    
    return (str(semitonesToIntervalName[pitchInterval]) + (f"(+{octaveInterval}')" if octaveInterval > 0 else ""))
