# Branch Monitor Simulator (Python)
Here we are simulating a DC bus of 12 V. Some branch currents are time-varying (PWM branch, time-varying-R branch, RL transient), so the currents aren’t flat, but the source is DC.

## Overview

- A DC source feeds N parallel branches:
	- Each branch has its own physics (pure R, RL, PWM’d resistor, or a resistor that varies with time).
	- This produces the true branch currents \( I_i(t) \).

- Only one measurement chain is available (shunt → amplifier → ADC):
	- An analog MUX selects which branch’s sense line goes to the ADC at each clock tick.
	- After a small settling time, the ADC samples that branch.

- Since not every branch is sampled at every instant, a reconstructor fills in the gaps for each branch between its sparse measurements:
	- **ZOH (Zero-Order Hold):** Holds the last value.
	- **α-β filter (light Kalman-style estimator):** Predicts with constant slope and corrects on each new sample.

- In parallel, a root sensor measures the total current (all branches together) continuously (with noise):
	- Comparing root vs sum of reconstructed branches gives a residual, indicating if the reconstruction is drifting.

- The simulator saves:
	- Time series
	- Plots
	- Metrics CSV (RMSEs)
	- These outputs help tune clock, settling, ADC bits, noise, and estimator gains.


    