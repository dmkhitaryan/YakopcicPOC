import numpy as np
import functions
import yakopcic_model


class Experiment:
    def __init__(self, sim_args, model, memristor_args):
        self.name = None
        self.frequency = sim_args["frequency"]
        self.dt = 1 / self.frequency

        self.simulation = {"x0": sim_args["x0"], "dt": self.dt}
        self.memristor_args = memristor_args
        self.memristor_args.update({"x0": sim_args["x0"]})
        self.memristor = model(**self.memristor_args)
        # self.memristor.print()

        self.functions = {
            "dxdt": self.memristor.dxdt,
            "I": self.memristor.I,
        }

        # print("Simulation:")
        # print(f"\tTime range [ {self.t_min}, {self.t_max} ]")
        # print(f"\tSamples {self.simulation['N']}")
        # print(f"\tInitial value of state variable {self.simulation['x0']}")


class YakopcicSET(Experiment):
    def __init__(self):
        super(YakopcicSET, self).__init__(
            sim_args={"frequency": 10e3, "x0": 0.0},
            model=yakopcic_model.YakopcicNew,
            memristor_args={
                "a1": 0.097,
                "a2": 0.097,
                "b": 0.05,
                "Ap": 0.1065893286 * 3e1,
                "An": 0.0118432587 * 3e1,
                "Vp": 0.5,
                "Vn": 0.5,
                "alphap": 1,
                "alphan": 1,
                "xp": 0.1,
                "xn": 0.242,
                "eta": 1
            },
        )
        self.name = "SET"
