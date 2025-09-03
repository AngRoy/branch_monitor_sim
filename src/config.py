from dataclasses import dataclass

@dataclass
class ADCConfig:
    vref: float = 3.3
    bits: int = 12
    amp_gain: float = 20.0
    r_shunt: float = 0.01
    branch_noise_rms: float = 0.005

@dataclass
class MUXConfig:
    f_clk: float = 1000.0
    t_settle: float = 200e-6

@dataclass
class SimulationConfig:
    duration: float = 3.0
    dt: float = 0.0005
    vdc: float = 12.0
    n_branches: int = 4
    root_noise_rms: float = 0.01
    alpha: float = 0.85
    beta: float = 0.005
