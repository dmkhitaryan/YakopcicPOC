from experiment_setup import *
from functions import *


def main():
    model = Memristor_Thomas
    iptVs = startup2(input_pulses)
    ptr = 120000 # pointer to cut off SET pulse points.
    time, voltage = interactive_iv(iptVs, model['dt'])
    x = np.zeros(voltage.shape, dtype=float)
    print("t: ", len(time), "v: ", len(voltage))

    for j in range(1, len(x)):
        x[j] = x[j - 1] + dxdt(voltage[j], x[j - 1], model['Ap'], model['An'], model['Vp'], model['Vn'], model['xp'],
                               model['xn'], model['alphap'], model['alphan'], 1) * model['dt']
        if x[j] < 0:
            x[j] = 0
        if x[j] > 1:
            x[j] = 1

    i = current(voltage, x, model['gmax_p'], model['bmax_p'], model['gmax_n'], model['bmax_n'], model['gmin_p'],
                model['bmin_p'],
                model['gmin_n'], model['bmin_n'])
    r = np.divide(voltage, i, out=np.zeros(voltage.shape, dtype=float), where=i != 0)

    plot_type = 1
    plot_images(plot_type, time, voltage, i, r, x, ptr, model)


if __name__ == "__main__":
    main()
