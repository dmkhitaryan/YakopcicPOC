import numpy as np


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
