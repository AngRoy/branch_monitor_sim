import os
import matplotlib.pyplot as plt

def plot_branch(times, true_series, est_series, branch_idx, out_dir):
    plt.figure(figsize=(9, 3.2))
    plt.plot(times, true_series, label=f"Branch {branch_idx} True")
    plt.plot(times, est_series, label=f"Branch {branch_idx} Est", linestyle="--")
    plt.xlabel("Time [s]"); plt.ylabel("Current [A]")
    plt.title(f"Branch {branch_idx}: True vs Estimated")
    plt.legend(); plt.tight_layout()
    os.makedirs(out_dir, exist_ok=True)
    plt.savefig(os.path.join(out_dir, f"branch_{branch_idx}.png")); plt.close()

def plot_total(times, sum_true, sum_est_zoh, sum_est_ab, out_dir):
    plt.figure(figsize=(9, 3.2))
    plt.plot(times, sum_true, label="Sum True")
    plt.plot(times, sum_est_ab, label="Sum Est (α-β)", linestyle="--")
    plt.plot(times, sum_est_zoh, label="Sum Est (ZOH)", linestyle=":")
    plt.xlabel("Time [s]"); plt.ylabel("Current [A]")
    plt.title("Total Current: True vs Reconstructed")
    plt.legend(); plt.tight_layout()
    os.makedirs(out_dir, exist_ok=True)
    plt.savefig(os.path.join(out_dir, "total_current.png")); plt.close()

def plot_residual(times, residual, out_dir):
    plt.figure(figsize=(9, 3.2))
    plt.plot(times, residual, label="Root-Measured - Sum(Est α-β)")
    plt.xlabel("Time [s]"); plt.ylabel("Residual [A]")
    plt.title("Residual against Root Sensor (diagnostics)")
    plt.legend(); plt.tight_layout()
    os.makedirs(out_dir, exist_ok=True)
    plt.savefig(os.path.join(out_dir, "residual.png")); plt.close()
