import argparse
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


# Given voltage and current numpy arrays, this function calculates the resistances.
# Those are then checked for segments of reading voltages (resistance is same value multiple times in a row).
# If true, add those into a separate list, with the duplicates removed after.
# Produce the resulting graph.
def calculate_resistance(voltage, current):
    resistance = voltage/current
    resistance_trim = []
    for i in range(0, len(resistance)-1):
        if resistance[i] == resistance[i+1]:
            resistance_trim.append(resistance[i])
    resistance_trim = list(dict.fromkeys(resistance_trim))
    plt.plot(range(0, len(resistance_trim)), resistance_trim, "o")
    plt.title("Trimmed resistance of Yakopcic memristor")
    plt.yscale("log")
    plt.show()


# Euler step-based solver that calculates the state variable and current for each time point.
# Return the resulting two arrays.
def solver2(f, time, dt, iv, v, args=[]):
    x_sol = [iv]
    current = [0.0]

    for i in range(1, len(time)):
        #current.append(I(time[i], v[i], x_sol[-1]))
        # print(x_sol[-1])
        x = euler_step(x_sol[-1], time[i], f, dt, v[i], args)
        # print("x:", x)
        if x < 0:
            x = 0
        if x > 1:
            x = 1

        x_sol.append(x)
    x_sol = np.array(x_sol)

    return x_sol

# Produces the voltage pulses based on the given inputs.
# Is currently hardcoded, to be adjusted for generalized inputs.
def input_volt(iptVs, dt):
    iptV1 = iptVs["1"]
    t = 0
    frequency = int(1 / dt)

    #print(time)
    t, v_total = generate_wave(iptV1, frequency, t)

    iptV2 = iptVs["2"]
    for i in range(0, 10):
        t, v_total = generate_wave(iptV2, frequency, t, v_total)

    iptV3 = iptVs["3"]
    for i in range(0, 10):
        t, v_total = generate_wave(iptV3, frequency, t, v_total)
    time = np.arange(0, t+dt, dt)
    #plt.plot(time, v_total)
    #plt.show()
    return time, v_total


def interactive_iv(iptVs, dt):
    t = 0
    v_total = []
    frequency = int(1 / dt)
    for iptV in iptVs.values():
        print("Printing:", iptV.get)
        for j in range(0, int(iptV['n_cycles'])):
            if j == 0:
                t, v_total = interactive_generate(iptV, frequency, t)
            else:
                t, v_total = interactive_generate(iptV, frequency, t, v_total)

    time = np.arange(0, t+dt, dt)
    plt.plot(time, v_total)
    plt.show()
    return time, v_total


def startup():
    iptVs = {}
    print("Please input your voltage pulses in the following format:\n",
          "t_rise t_on t_fall t_off V_on V_off n_cycles")
    wave_number = 0
    while True:
        try:
            t_rise, t_on, t_fall, t_off, V_on, V_off, n_cycles = map(float, input("Enter a wave or -1 to end inputs:\n").split())
            if t_rise == -1:
                print("Inputs collected.")
                return iptVs
            iptV = {"t_rise": t_rise, "t_on": t_on, "t_fall": t_fall, "t_off": t_off, "V_on": V_on, "V_off": V_off,
                    "n_cycles": n_cycles}
            print(iptV)
            iptVs["{}.format(wave_number)"] = iptV
            continue
        except ValueError:
            print("Please provide correct inputs.")
            continue


def main():
    #iptVs = startup()
    time, voltage = input_volt(inputVs, dt)
    #time, voltage = interactive_iv(iptVs, dt)

    x = solver2(dxdt, time, dt, 0.0, voltage)
    print("time length:", len(time), "\n", "voltage length:", len(voltage), "\n", "x length:", len(x))
    i = I(time, voltage, x)
    #calculate_resistance(voltage, i)
    plt.plot(time, voltage/i)
    plt.title("Resistance of Yakopcic memristor")
    plt.show()


if __name__ == "__main__":
    main()