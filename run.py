import argparse

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

inputV1 = {"t_rise": .0025, "t_on": 119, "t_fall": .0025, "t_off": 0, "V_on": 1.0, "V_off": 0}
inputV2 = {"t_rise": .45, "t_on": 0.1, "t_fall": .45, "t_off": 1, "V_on": -3, "V_off": -.1}
inputV3 = {"t_rise": .45, "t_on": 0.1, "t_fall": .45, "t_off": 1, "V_on": 1, "V_off": -.1}
inputVs = {"1": inputV1, "2": inputV2, "3": inputV3}


def startup():
    iptVs = {}
    print("Please input your voltage pulses in the following format:\n",
          "t_rise t_on t_fall t_off V_on V_off n_cycles")
    wave_number = 1
    while True:
        try:
            t_rise, t_on, t_fall, t_off, V_on, V_off, n_cycles = map(float, input(
                "Enter a wave or -1 to end inputs:\n").split())
            if t_rise == -1:
                print("Inputs collected.")
                return iptVs
            iptV = {"t_rise": t_rise, "t_on": t_on, "t_fall": t_fall, "t_off": t_off, "V_on": V_on, "V_off": V_off,
                    "n_cycles": int(n_cycles)}
            #print(iptV)
            iptVs["{}".format(wave_number)] = iptV
            wave_number += 1
            continue
        except ValueError:
            print("Please provide correct inputs.")
            continue


def main():
    iptVs = startup()
    time, voltage = interactive_iv(iptVs, dt)

    x = solver2(dxdt, time, dt, 0.0, voltage)
    print("time length:", len(time), "\n", "voltage length:", len(voltage), "\n", "x length:", len(x))
    i = I(time, voltage, x)
    # calculate_resistance(voltage, i)
    plt.plot(time, voltage/i)
    plt.title("Resistance of Yakopcic memristor")
    plt.show()


if __name__ == "__main__":
    main()