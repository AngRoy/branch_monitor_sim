from dataclasses import dataclass
import math

@dataclass
class BranchBase:
    i_true: float = 0.0
    def update(self, t: float, dt: float, v_src: float) -> None:
        raise NotImplementedError

@dataclass
class ResistiveBranch(BranchBase):
    R: float = 4.0
    def update(self, t: float, dt: float, v_src: float) -> None:
        self.i_true = v_src / self.R

@dataclass
class RLBranch(BranchBase):
    R: float = 2.0
    L: float = 10e-3
    def update(self, t: float, dt: float, v_src: float) -> None:
        di = (v_src - self.R * self.i_true) / self.L * dt
        self.i_true += di

@dataclass
class PWMSwitchingResistiveBranch(BranchBase):
    R_on: float = 3.0
    f_pwm: float = 50.0
    duty: float = 0.6
    phase: float = 0.0
    def update(self, t: float, dt: float, v_src: float) -> None:
        frac = (t * self.f_pwm + self.phase) % 1.0
        on = frac < self.duty
        self.i_true = v_src / self.R_on if on else 0.0

@dataclass
class TimeVaryingResistiveBranch(BranchBase):
    R0: float = 5.0
    f_mod: float = 2.0
    depth: float = 0.5
    def update(self, t: float, dt: float, v_src: float) -> None:
        R_t = self.R0 * (1.0 + self.depth * math.sin(2.0 * math.pi * self.f_mod * t))
        self.i_true = v_src / R_t
