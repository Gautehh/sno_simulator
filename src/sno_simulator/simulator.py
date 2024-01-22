from io import TextIOWrapper
from sno import SnøLag


def snø_simulator(file: TextIOWrapper, snø_lag: SnøLag):
    vann_ute_av_systemet = []
    snødybde = []
    tid = []
    for line in file.readlines():
        vann = 0
        time, nedbør, tempratur = line.split(";")
        nedbør = float(nedbør)
        temp = float(tempratur)
        if temp < 0:
            snø_lag.snøfall(nedbør)
            snø_lag.is_dannelse()
        else:
            vann = snø_lag.smelting(temp)
        vann_ute_av_systemet.append(vann)
        snødybde.append(snø_lag.dybde)
        tid.append(time)
    return tid, vann_ute_av_systemet, snødybde
