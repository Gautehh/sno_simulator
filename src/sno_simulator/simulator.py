from io import TextIOWrapper
from sno import SnøLag


def snø_simulator(file: TextIOWrapper, lag: SnøLag):
    vann_i_systemet = []
    snødybde = []
    tid = []
    for line in file.readlines():
        vann = 0
        time, nedbør, temp = line.split(";")
        nedbør = float(nedbør)
        temp = float(temp)
        if temp < 0:
            lag.snøfall(nedbør)
            lag.minus()
        else:
            vann = lag.smelting(temp)
        vann_i_systemet.append(vann)
        snødybde.append(lag.dybde)
        tid.append(time)
    return tid, vann_i_systemet, snødybde
