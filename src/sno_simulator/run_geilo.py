from matplotlib import pyplot as plt
import os
from simulator import snø_simulator
from sno import SnøLag

snø_lag = SnøLag(0.1, 0.1)
current_dir = os.path.dirname(os.path.realpath(__file__))

def main():
    with open(f"{current_dir}/assets/sno_geilo.csv") as f:
        tid, vann_i_systemet, snødybde = snø_simulator(f, snø_lag)
    plt.plot(vann_i_systemet)
    plt.plot(snødybde)
    plt.show()
    d = 10

main()
