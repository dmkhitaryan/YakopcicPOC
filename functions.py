import numpy as np
import os
import scipy.signal
from scipy import interpolate
from order_of_magnitude import order_of_magnitude

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.animation as animation


class InputVoltage():
    def __init__(self, shape=None, vp=None, vn=None, frequency=None, period=None, t_max=None):
        self.shape = shape
        self.vp = vp
        self.vn = vn if vn else vp
        self.frequency = 1 / period if period else frequency
        self.period = 1 / frequency if frequency else period
        self.t_max = t_max

    def __call__(self, t, read):
        pass

    def print(self, start="\t"):
        start_lv2 = start + "\t"
        print(f"{start_lv2}Shape {self.shape}")
        print(f"{start_lv2}Magnitude +{self.vp} / -{self.vn} V")
        print(f"{start_lv2}Frequency {self.frequency} Hz")
        print(f"{start_lv2}Period {self.period} s")


class Triangle(InputVoltage):
    def __init__(self, vp=1, vn=None, frequency=None, period=None, t_max=0):
        assert frequency or period
        assert t_max > 0

        super(Triangle, self).__init__("triangle", vp, vn, frequency, period, t_max)

    def __call__(self, t, read=False):
        pos = self.vp * np.abs(scipy.signal.sawtooth(2 * self.frequency * np.pi * t + np.pi / 2, 0.5))
        neg = -1 * self.vn * np.abs(scipy.signal.sawtooth(2 * self.frequency * np.pi * t + np.pi / 2, 0.5))

        if isinstance(t, np.ndarray) and len(t) > 1:
            pos[len(pos) // 2:] *= -1
        elif t > self.t_max / 2:
            pos *= -1

        v = np.where(pos > 0, pos, neg)

        return v


class SETPulse(InputVoltage):
    def __init__(self, vp=1, vn=None, frequency=None, period=None, t_max=0):
        assert frequency or period
        assert t_max > 0

        super(SETPulse, self).__init__("SETPulse", vp, vn, frequency, period, t_max)

    def __call__(self, t, read=False):
        v = np.ones(t.size)
        return v


class DepressionPulse(InputVoltage):
    def __init__(self, vp=1, vn=None, frequency=None, period=None, t_max=0):
        assert frequency or period
        assert t_max > 0

        super(DepressionPulse, self).__init__("DepressionPulse", vp, vn, frequency, period, t_max)

    def __call__(self, t, read=None):
        read = False if read is None else read
        if read:
            v = -1 * self.vp * np.abs(scipy.signal.sawtooth(np.pi * t + np.pi / 2, 0.5))
        else:
            v = -1 * self.vn * np.abs(scipy.signal.sawtooth(np.pi * t + np.pi / 2, 0.5))

        return v


def generate_wave(iv, frequency, t, base=None):
    base = np.array([0]) if base is None else base
    t += (iv["t_rise"] + iv["t_fall"] + iv["t_on"] + iv["t_off"])
    v1 = np.linspace(iv["V_off"], iv["V_on"], int(iv["t_rise"] * frequency))
    v2 = iv["V_on"] * np.ones(int(iv["t_on"] * frequency))
    v3 = np.linspace(iv["V_on"], iv["V_off"], int(iv["t_fall"] * frequency))
    v4 = np.array([]) if iv["t_off"] == 0 else iv["V_off"] * np.ones(int(iv["t_off"] * frequency))
    vtotal = np.concatenate((base, v1, v2, v3, v4))
    return t, vtotal


def interactive_generate(iv, frequency, t, base=None):
    base = np.array([0]) if base is None else base
    t += (float(iv["t_rise"]) + float(iv["t_fall"]) + float(iv["t_on"]) + float(iv["t_off"]))
    v1 = np.linspace(float(iv["V_off"]), float(iv["V_on"]), int(iv["t_rise"] * frequency))
    v2 = float(iv["V_on"]) * np.ones(int(iv["t_on"] * frequency))
    v3 = np.linspace(float(iv["V_on"]), float(iv["V_off"]), int(iv["t_fall"] * frequency))
    v4 = np.array([]) if float(iv["t_off"]) == 0 else float(iv["V_off"]) * np.ones(int(iv["t_off"] * frequency))
    vtotal = np.concatenate((base, v1, v2, v3, v4))
    return t, vtotal
