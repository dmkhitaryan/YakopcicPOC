import numpy as np

import yakopcic_model
import tkinter as tk
from experiment_setup import *
from functions import *
from yakopcic_model import *

experiment = YakopcicSET()
V = experiment.functions["V"]
I = experiment.functions["I"]
T = experiment.simulation["time"]
dxdt = experiment.functions["dxdt"]
dt = experiment.simulation["dt"]
print(len(T))


def solver(f, time, dt, start, V, args=None):
    second = 0
    if args is None:
        args = []
    x_sol = [start]
    voltage = [V(time[0])]
    current = [I(time[0], start)]
    for t in time[1:]:
        if t == 1:
            print("!!!")
            experiment.memristor.V = DepressionPulse(**{"frequency": 100, "vp": 4, "vn": 1, "t_max": experiment.t_max})
            V = experiment.memristor.V
            print(V)
            voltage.append(V(t))
            second += 1
        if t < 1:
            x = euler_step(x_sol[-1], t, dxdt, dt, args)
            x_sol.append(x)
            current.append(I(t, x))
            voltage.append(V(t))
        else:
            for m in range(0, 3):
                if 1 + (2 * m) <= t < 1 + (2 * m + 1):
                    x = euler_step(x_sol[-1], t, f, dt, args)
                    x = float(x)
                    x_sol.append(x)
                    # voltage_array[np.where(T == k)] = Voltage(k, read=True)
                    current.append(I(t, x, read=True))
                    voltage.append(V(t, read=True))
                if 1 + (2 * m + 1) <= t < 1 + (2 * m + 2):
                    x = euler_step(x_sol[-1], t, f, dt, args)
                    x = float(x)
                    x_sol.append(x)
                    # voltage_array[np.where(T == k)] = Voltage(k, read=False)
                    current.append(I(t, x, read=False))
                    voltage.append(V(t, read=False))

    plt.plot(time, voltage)
    plt.show()


# solver(dxdt, T, dt, 0, V)
inputV1 = {"t_rise": .0025, "t_on": 9.95, "t_fall": .0025, "t_off": 0, "V_on": 1.0, "V_off": 0}
inputV2 = {"t_rise": .45, "t_on": 0.1, "t_fall": .45, "t_off": .1, "V_on": -2, "V_off": -1}
inputVs = {"1": inputV1, "2": inputV2}


# print(inputV1["V_on"])


def solver2(f, time, dt, iv, v, args=[]):
    x_sol = [iv]
    current = [0.0]

    for i in range(1, len(time)):
        current.append(I(time[i], v[i], x_sol[-1]))
        # print(x_sol[-1])
        x = euler_step(x_sol[-1], time[i], f, dt, v[i], args)
        # print("x:", x)
        if x < 0:
            x = 0
        if x > 1:
            x = 1

        x_sol.append(x)
    x_sol = np.array(x_sol)

    return x_sol, current


def input_volt(iptVs, dt):
    iptV1 = iptVs["1"]
    t = 0
    frequency = int(1 / dt)

    #print(time)
    t, v_total = generate_wave(iptV1, frequency, t)

    iptV2 = iptVs["2"]
    for i in range(0, 10):
        t, v_total = generate_wave(iptV2, frequency, t, v_total)
    time = np.arange(0, t, dt)
    #plt.plot(time, v_total)
    #plt.show()
    return time, v_total


time, voltage = input_volt(inputVs, dt)
print(len(time), len(voltage))
x, i = solver2(dxdt, time, dt, 0.0, voltage)
plt.plot(time, voltage/i)
plt.show()
