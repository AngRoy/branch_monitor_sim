import os
from src.config import SimulationConfig, ADCConfig, MUXConfig
from src.simulator import run_sim
from src.plotting import plot_branch, plot_total, plot_residual

def main():
    sim_cfg = SimulationConfig(duration=3.0, dt=0.0005, vdc=12.0, n_branches=4, root_noise_rms=0.01, alpha=0.85, beta=0.005)
    adc_cfg = ADCConfig(vref=3.3, bits=12, amp_gain=20.0, r_shunt=0.01, branch_noise_rms=0.005)
    mux_cfg = MUXConfig(f_clk=1000.0, t_settle=200e-6)
    outputs = run_sim(sim_cfg, adc_cfg, mux_cfg)
    out_dir = "outputs"; os.makedirs(out_dir, exist_ok=True)
    outputs.metrics_df.to_csv(os.path.join(out_dir, "summary_metrics.csv"), index=False)
    for i in range(sim_cfg.n_branches):
        plot_branch(outputs.times, outputs.i_true[i], outputs.i_hat_ab[i], i, out_dir)
    plot_total(outputs.times, outputs.i_sum_true, outputs.i_sum_zoh, outputs.i_sum_ab, out_dir)
    residual = outputs.i_root_meas - outputs.i_sum_ab
    plot_residual(outputs.times, residual, out_dir)
    print("Saved outputs in", os.path.abspath(out_dir))

if __name__ == "__main__":
    main()
