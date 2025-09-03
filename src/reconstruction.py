from dataclasses import dataclass
from typing import List

@dataclass
class ZOHState:
    value: float = 0.0
class ZOHReconstructor:
    def __init__(self, n_branches: int):
        self.state: List[ZOHState] = [ZOHState() for _ in range(n_branches)]
    def predict(self, dt: float) -> None:
        pass
    def update(self, ch: int, z: float, t_now: float) -> None:
        self.state[ch].value = z
    def values(self) -> List[float]:
        return [s.value for s in self.state]

@dataclass
class ABState:
    x: float = 0.0
    xdot: float = 0.0
    last_t: float = 0.0
class AlphaBetaReconstructor:
    def __init__(self, n_branches: int, alpha: float, beta: float):
        self.alpha = alpha
        self.beta = beta
        self.state: List[ABState] = [ABState() for _ in range(n_branches)]
    def predict(self, dt: float) -> None:
        for s in self.state:
            s.x += s.xdot * dt
    def update(self, ch: int, z: float, t_now: float) -> None:
        s = self.state[ch]
        dt_meas = max(1e-9, t_now - s.last_t)
        x_pred = s.x + s.xdot * dt_meas
        r = z - x_pred
        s.x = x_pred + self.alpha * r
        s.xdot = s.xdot + (self.beta / dt_meas) * r
        s.last_t = t_now
    def values(self) -> List[float]:
        return [s.x for s in self.state]
