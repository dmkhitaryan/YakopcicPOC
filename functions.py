import numpy as np
import matplotlib.pyplot as plt
from yakopcic_model import *

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
                t, v_total = generate_wave(iptV, frequency, t)
            else:
                t, v_total = generate_wave(iptV, frequency, t, v_total)

    time = np.arange(0, t+dt, dt)
    plt.plot(time, v_total)
    plt.show()
    return time, v_total


def generate_wave(iv, frequency, t, base=None):
    base = np.array([0]) if base is None else base
    t += (iv["t_rise"] + iv["t_fall"] + iv["t_on"] + iv["t_off"])
    v1 = np.linspace(iv["V_off"], iv["V_on"], int(iv["t_rise"] * frequency))
    v2 = iv["V_on"] * np.ones(int(iv["t_on"] * frequency))
    v3 = np.linspace(iv["V_on"], iv["V_off"], int(iv["t_fall"] * frequency))
    v4 = np.array([]) if iv["t_off"] == 0 else iv["V_off"] * np.ones(int(iv["t_off"] * frequency))
    vtotal = np.concatenate((base, v1, v2, v3, v4))
    return t, vtotal
