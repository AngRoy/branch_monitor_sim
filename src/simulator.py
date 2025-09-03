from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
import pandas as pd
from .config import SimulationConfig, ADCConfig, MUXConfig
from .branch import BranchBase, ResistiveBranch, RLBranch, PWMSwitchingResistiveBranch, TimeVaryingResistiveBranch
from .hardware import MeasurementChain, RootSensor
from .scheduler import RoundRobinScheduler
from .reconstruction import ZOHReconstructor, AlphaBetaReconstructor
from .metrics import rmse

@dataclass
class SimulationOutputs:
    times: np.ndarray
    i_true: np.ndarray
    i_hat_zoh: np.ndarray
    i_hat_ab: np.ndarray
    i_sum_true: np.ndarray
    i_sum_zoh: np.ndarray
    i_sum_ab: np.ndarray
    i_root_meas: np.ndarray
    metrics_df: pd.DataFrame

def default_branches(n: int) -> List[BranchBase]:
    pattern: List[BranchBase] = [
        ResistiveBranch(R=4.0),
        RLBranch(R=2.0, L=10e-3),
        PWMSwitchingResistiveBranch(R_on=3.0, f_pwm=50.0, duty=0.6, phase=0.0),
        TimeVaryingResistiveBranch(R0=5.0, f_mod=2.0, depth=0.5),
    ]
    out: List[BranchBase] = []
    import copy
    for i in range(n):
        out.append(copy.deepcopy(pattern[i % len(pattern)]))
    return out

def run_sim(cfg: SimulationConfig, adc_cfg: ADCConfig, mux_cfg: MUXConfig, branches: List[BranchBase] | None = None) -> SimulationOutputs:
    if branches is None: branches = default_branches(cfg.n_branches)
    N = cfg.n_branches
    M = int(np.floor(cfg.duration / cfg.dt))
    times = np.arange(M) * cfg.dt
    i_true = np.zeros((N, M)); i_hat_zoh = np.zeros((N, M)); i_hat_ab = np.zeros((N, M))
    i_sum_true = np.zeros(M); i_sum_zoh = np.zeros(M); i_sum_ab = np.zeros(M); i_root_meas = np.zeros(M)
    meas_chain = MeasurementChain(cfg=adc_cfg); root = RootSensor(noise_rms=cfg.root_noise_rms)
    scheduler = RoundRobinScheduler.from_params(n_channels=N, cfg=mux_cfg)
    zoh = ZOHReconstructor(n_branches=N); ab = AlphaBetaReconstructor(n_branches=N, alpha=cfg.alpha, beta=cfg.beta)
    pending: List[Tuple[float, int]] = []
    for k, t in enumerate(times):
        for i, br in enumerate(branches):
            br.update(t, cfg.dt, cfg.vdc); i_true[i, k] = br.i_true
        i_sum_true[k] = np.sum(i_true[:, k]); i_root_meas[k] = root.measure(i_sum_true[k])
        switched, ch, tsample = scheduler.step(t)
        if switched and tsample is not None and tsample <= cfg.duration:
            pending.append((tsample, ch))
        remain = []
        for tsmp, c in pending:
            if tsmp <= t + 1e-12:
                z = meas_chain.measure_current(i_true[c, k])
                zoh.update(c, z, t_now=t); ab.update(c, z, t_now=t)
            else: remain.append((tsmp, c))
        pending = remain
        zoh.predict(cfg.dt); ab.predict(cfg.dt)
        vals_zoh = zoh.values(); vals_ab = ab.values()
        for i in range(N):
            i_hat_zoh[i, k] = vals_zoh[i]; i_hat_ab[i, k] = vals_ab[i]
        i_sum_zoh[k] = np.sum(i_hat_zoh[:, k]); i_sum_ab[k] = np.sum(i_hat_ab[:, k])
    rows = []
    for i in range(N):
        rows.append({"Branch": i, "RMSE_AB [A]": rmse(i_true[i], i_hat_ab[i]), "RMSE_ZOH [A]": rmse(i_true[i], i_hat_zoh[i]), "Mean True [A]": float(np.mean(i_true[i])), "Std True [A]": float(np.std(i_true[i]))})
    rows.append({"Branch": "SUM", "RMSE_AB [A]": rmse(i_sum_true, i_sum_ab), "RMSE_ZOH [A]": rmse(i_sum_true, i_sum_zoh), "Mean True [A]": float(np.mean(i_sum_true)), "Std True [A]": float(np.std(i_sum_true))})
    metrics_df = pd.DataFrame(rows)
    return SimulationOutputs(times, i_true, i_hat_zoh, i_hat_ab, i_sum_true, i_sum_zoh, i_sum_ab, i_root_meas, metrics_df)
