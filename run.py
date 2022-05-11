import sys

import matplotlib.pyplot as plt
import numpy as np
import yakopcic_model
from experiment_setup import *
from functions import *
from yakopcic_model import *

experiment = YakopcicSET()
I = experiment.functions["I"]
dxdt = experiment.functions["dxdt"]
dt = experiment.simulation["dt"]


def startup2():
    iptVs = {}
    with open(sys.argv[1], "r") as input_file:
        lines = input_file.readlines()

    wave_number = 1
    for line in lines:
        t_rise, t_on, t_fall, t_off, V_on, V_off, n_cycles = map(float, line.split())
        iptV = {"t_rise": t_rise, "t_on": t_on, "t_fall": t_fall, "t_off": t_off, "V_on": V_on, "V_off": V_off,
                "n_cycles": int(n_cycles)}
        iptVs["{}".format(wave_number)] = iptV
        wave_number += 1

    return iptVs


def main():
    iptVs = startup2()
    time, voltage = interactive_iv(iptVs, dt)
    x = solver2(dxdt, time, dt, 0.0, voltage)
    i = I(time, voltage, x)
    plt.plot(time[:], (voltage[:]/i[:])*10)
    plt.title("Resistance of the Yakopcic memristor")
    plt.yscale("log")
    plt.show()


if __name__ == "__main__":
    main()