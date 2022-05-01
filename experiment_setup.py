import numpy as np
import functions
import yakopcic_model

class Experiment:
    def __init__(self, sim_args, model, input_function, memristor_args, input_args):
        self.name = None
        self.t_max = sim_args["t_max"]
        self.frequency = sim_args["frequency"]

        self.t_min = 0

        self.simulation = {
            "x0": sim_args["x0"]
        }
        self.recalculate_time(self.t_max)

        self.input_args = input_args
        self.input_args.update({"t_max": self.t_max})
        self.input_function = input_function(**self.input_args)

        self.memristor_args = memristor_args
        self.memristor_args.update({"x0": sim_args["x0"]})
        self.memristor = model(self.input_function, **self.memristor_args)
        self.memristor.print()

        self.functions = {
            "dxdt": self.memristor.dxdt,
            "V": self.memristor.V,
            "I": self.memristor.I,
        }

        self.fitting = {
            "noise": 10
        }

        print("Simulation:")
        print(f"\tTime range [ {self.t_min}, {self.t_max} ]")
        print(f"\tSamples {self.simulation['N']}")
        print(f"\tInitial value of state variable {self.simulation['x0']}")

    def recalculate_time(self, t_max):
        self.dt = 1 / self.frequency
        self.t_max = t_max
        self.simulation["dt"] = self.dt
        self.simulation["t_min"] = 0
        self.simulation["t_max"] = t_max
        self.simulation["time"] = np.arange(self.t_min, t_max + self.dt, self.dt)
        self.simulation["N"] = (self.t_max - self.t_min) * self.frequency

    def fit_memristor(self):
        pass


class YakopcicSET(Experiment):
    def __init__(self):
        super(YakopcicSET, self).__init__(
            sim_args={"t_max": 7, "frequency": 10e3, "x0": 0.0},
            model=yakopcic_model.YakopcicNew,
            input_function=functions.SETPulse,
            memristor_args={
                "a1": 0.097,
                "a2": 0.097,
                "b": 0.05,
                "Ap": 90/844.3632,
                "An": 10/844.3632,
                "Vp": 0.5,
                "Vn": 0.5,
                "alphap": 1,
                "alphan": 1,
                "xp": 0.1,
                "xn": 0.242,
                "eta": 1
            },
            input_args={"frequency": 100, "vp": 1, "vn": 1},
        )

        self.name = "SET"


class YakopcicDepression(Experiment):
    def __init__(self):
        super(YakopcicDepression, self).__init__(
            sim_args={"t_max": 5, "frequency": 1e4, "x0": 0.0},
            model=models.Yakopcic,
            input_function=functions.DepressionPulse,
            memristor_args={
                "a1": 0.097,
                "a2": 0.097,
                "b": 0.05,
                "Ap": 10.0,
                "An": 90.0,
                "Vp": 0.5,
                "Vn": 0.5,
                "alphap": 1,
                "alphan": 1,
                "xp": 0.1,
                "xn": 0.242,
                "eta": 1
            },
            input_args={"frequency": 100, "vp": 4, "vn": 1},
        )

        self.name = "Depression"