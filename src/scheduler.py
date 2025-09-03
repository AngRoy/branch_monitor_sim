from dataclasses import dataclass
from typing import Tuple
from .hardware import AnalogMUX
from .config import MUXConfig

@dataclass
class RoundRobinScheduler:
    mux: AnalogMUX
    @classmethod
    def from_params(cls, n_channels: int, cfg: MUXConfig) -> "RoundRobinScheduler":
        return cls(AnalogMUX(n_channels=n_channels, cfg=cfg))
    def step(self, t_now: float) -> Tuple[bool, int, float]:
        return self.mux.step(t_now)
