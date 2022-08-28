# Yakopcic Proof of Concept
This project is intended to serve as a proof of concept that Yakopcic memristor model
(https://ieeexplore.ieee.org/document/8695752) can "learn". Namely, the expectation is 
that its behaviour (resistance) in response to depression/potentiation voltage pulses will 
match that of the memristor described in: https://www.frontiersin.org/articles/10.3389/fnins.2020.627276/full#h3. 
A short description of each file and its purpose is provided below.

## Experiment Setup (experiment_setup.py)
Responsible for the setup of the experiment and provision of parameters to the memristor.
Also contains the input strings for the voltage pulses to be simulated.


## Functions (functions.py)
Contains all the functions used in the project that are not related to initialization or the 
experiment setup. 

`interactive_iv` function creates voltage pulses based on parameters such as _on_ and _off_ voltages among others.
When done, it concatenates all the pulses, as well as creates the resulting _time_ array.  


`generate_wave` function is responsible for actually constructing the array for the 
voltage pulse(s), depending on the set number of cycles. This involves creating four segments:
rising, on-time, falling, and off-time, which are concatenated (with the total array if not the
first pulse) and returned after.  


`solver2` function is used to calculate the state variable with the differential equation 
provided by a memristor model (namely, Yakopcic). Given a starting point _x0_, the solver uses the 
Euler step to iteratively calculate the state variable _x(t)_ using the voltage _v(t)_ and
the previous state variable _x(t-1)_.

`plot_images` takes data such as voltage and current among others and uses those to produce visual
output of the results. This function can also generate debug plots, depending on the supplied input.

## Running the Project (run.py)
To run the pulse experiment, execture the _run.py_ python file. By default, the script is set to the
original (*Memristor_Thomas*), but also supports the newer iteration, based on the work by Dima (2022).

## Input Formatting
The formatting order in the voltage input follows the order below:
* `t_rise`**(s)**: time for the voltage to go from 'off' to 'on' state.
* `t_on`**(s)**: time the voltage remains in the 'on' state.
* `t_fall`**(s)** time for the voltage to go from 'on' to 'off' state.
* `t_off`**(s)**: time the voltage remains in the 'off' state.
* `V_on`**(V)**:  the voltage during the 'on' state.
* `V_off`**(V)**: the voltage during the 'off' state.
* `n_cycles`: the number of times the pulse is repeated.