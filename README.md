# Yakopcic Proof of Concept
This project is intended to serve as a proof of concept that Yakopcic memristor model
(https://ieeexplore.ieee.org/document/8695752) can "learn". Namely, the expectation is 
that its behaviour (resistance) in response to depression/potentiation voltage pulses will 
match that of the memristor described in: https://www.frontiersin.org/articles/10.3389/fnins.2020.627276/full#h3. 
A short description of each file and its purpose is provided below.

## Experiment setup (experiment_setup.py)
Responsible for the setup of the experiment and provision of parameters to the memristor.
Namely, the `Experiment` class is the generalized setup that, when called, takes a number of values,
such as the memristor model and the time step among others, while the `YakopcicSET`
class provides those. For the current objective, just the `YakopcicSET` is enough.

## Functions (functions.py)
Contains all the functions used in the project that are not related to initialization or the 
experiment setup. 

The `input_volt/interactive_iv` functions essentially do the same thing:
both create voltage pulses based on parameters such as 'on' and 'off' voltages among others.
The difference is that the first function is hardcoded (for testing purposes), whereas the 
second one is the generalised solution for future uses.  


The `generate_wave` function is responsible for actually constructing the array for the 
voltage pulse(s), depending on the set number of cycles. This involves creating four segments:
rising, on-time, falling, and off-time, which are concatenated (with the total array if not the
first pulse) and returned after.  


The `solver2` function is used to calculate the state variable with the differential equation 
provided by a memristor model (namely, Yakopcic). Given a starting point _x0_, the solver uses the 
Euler step to iteratively calculate the state variable _x(t)_ using the voltage _v(t)_ and
the previous state variable _x(t-1)_.

## Yakopcic Memristor Model (yakopcic_model.py)
Contains the old and new (more interest is on the latter) Yakopcic memristor models. This involves
setting a multitude of parameters (e.g., _Vp_ and _Vn_ defining positive and negative voltage 
thresholds beyond which voltages begin altering the state variable), as well as defining numerous
functions, for example, the current _I_. For more information on the specifics of the functions 
within, refer to the docstrings within the fire.