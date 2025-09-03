from dataclasses import dataclass
import numpy as np
from typing import Tuple
from .config import ADCConfig, MUXConfig

@dataclass
class AnalogMUX:
    n_channels: int
    cfg: MUXConfig
    ch: int = -1
    next_switch_time: float = 0.0
    def step(self, t_now: float) -> Tuple[bool, int, float]:
        period = 1.0 / self.cfg.f_clk
        if t_now + 1e-12 >= self.next_switch_time:
            self.ch = (self.ch + 1) % self.n_channels
            self.next_switch_time += period
            return True, self.ch, t_now + self.cfg.t_settle
        return False, self.ch, None

@dataclass
class MeasurementChain:
    cfg: ADCConfig
    @property
    def lsb(self) -> float:
        return self.cfg.vref / (2**self.cfg.bits - 1)
    def measure_current(self, i_true: float) -> float:
        v_shunt = i_true * self.cfg.r_shunt
        v_amp = v_shunt * self.cfg.amp_gain
        v_noise = np.random.normal(0.0, self.cfg.branch_noise_rms * self.cfg.r_shunt * self.cfg.amp_gain)
        v_in = np.clip(v_amp + v_noise, 0.0, self.cfg.vref)
        code = int(round(v_in / self.lsb))
        code = max(0, min(code, 2**self.cfg.bits - 1))
        v_q = code * self.lsb
        return (v_q / self.cfg.amp_gain) / self.cfg.r_shunt

@dataclass
class RootSensor:
    noise_rms: float = 0.01
    def measure(self, i_total_true: float) -> float:
        return i_total_true + np.random.normal(0.0, self.noise_rms)
