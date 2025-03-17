import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import null_space
from scipy.optimize import minimize
from APpositions import generate_APs

### PHYSICAL CONSTANTS (taken from section 5 of the paper)
phi_half = 60
m = -np.log(2) / np.log(np.cos(np.radians(phi_half)))
IDC = 1
eta = 1
R = 1
T = 1
A_PD = 1
sigma2 = 10 ** -9.833

def channel_gain(tx, rx):
    """Compute LoS channel gain between transmitter and receiver."""
    tx_normal = np.array([0, 0, -1])
    rx_normal = np.array([0, 0, +1])
    tx_to_rx = np.array(rx) - np.array(tx)
    distance = np.linalg.norm(tx_to_rx)
    tx_to_rx_normalized = tx_to_rx / distance
    cos_phi = np.dot(tx_normal, tx_to_rx_normalized)
    cos_psi = np.dot(rx_normal, -tx_to_rx_normalized)
    return cos_phi * cos_psi

def compute_null_space(AP_positions, AED_positions):
    """Compute a basis for the null space of the AEDs' channel matrix."""
    H_AED = np.array([[channel_gain(AP, AED) for AP in AP_positions] for AED in AED_positions])
    return null_space(H_AED)

def compute_snr(x, y, AP_positions, w):
    """Compute SNR at a given (x, y) point."""
    rx_position = np.array([x, y, 0])
    h_k = np.array([channel_gain(AP, rx_position) for AP in AP_positions])
    snr = (IDC**2 * (w.T @ h_k) ** 2) / sigma2
    return snr

PED_sampleResolution = 0.3
def generate_sampled_positions():
    """Generate positions for PEDs"""
    x_vals = np.linspace(0, 1, int(1 / PED_sampleResolution))
    y_vals = np.linspace(0, 1, int(1 / PED_sampleResolution))
    PED_positions = [(x, y) for x in x_vals for y in y_vals]
    return PED_positions

def compute_beamforming_vector(AP_positions, AU_position, AED_positions, PED_positions):
    """Compute w that maximizes AU gain while making AEDs gains zero and minimizing peak SNR."""
    null_basis = compute_null_space(AP_positions, AED_positions)
    h_AU = np.array([channel_gain(AP, AU_position) for AP in AP_positions])
    
    # Initial beamforming vector in null space
    w_init = null_basis @ (null_basis.T @ h_AU)
    w_init = w_init / np.linalg.norm(w_init)

    def objective(w):
        """We want to minimize peak SNR at PED positions"""
        w = np.array(w)
        peak_snr = max(compute_snr(x, y, AP_positions, w) for x, y in PED_positions)
        return peak_snr  # Minimize highest SNR outside AU
    
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.dot(w, h_AU) - 1},  # Keep AU SNR maximized
    ]

    result = minimize(objective, w_init, constraints=constraints, method='trust-constr')
    
    return result.x / np.linalg.norm(result.x)

def plot_PEDs(PED_positions):
    plt.figure(figsize=(5, 5))
    PEDs_x = [pos[0] for pos in PED_positions]
    PEDs_y = [pos[1] for pos in PED_positions]
    plt.scatter(PEDs_x, PEDs_y, color='black', marker='.', label="Sampled PED Positions", s=5)
    plt.title(f"Sampling possible PED positions")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.legend()
    plt.show()

def plot_snr(N, AP_positions, w, AU_position, AED_positions):
    """Plot SNR heatmap with AU, AED, and sampled PED positions."""
    grid_res = 0.05
    x_vals = np.linspace(0, 1, int(1 / grid_res))
    y_vals = np.linspace(0, 1, int(1 / grid_res))
    snr_grid = np.zeros((len(x_vals), len(y_vals)))

    for i, x in enumerate(x_vals):
        for j, y in enumerate(y_vals):
            snr_grid[i, j] = compute_snr(x, y, AP_positions, w)

    X, Y = np.meshgrid(x_vals, y_vals)
    plt.figure(figsize=(5, 5))
    plt.contourf(X, Y, snr_grid.T, levels=20, cmap='jet')
    plt.colorbar(label="SNR")
    
    # Mark AU and AEDs
    plt.scatter(*AU_position[:2], color='yellow', marker='o', label="AU", s=100)
    AEDs_x = [AED[0] for AED in AED_positions]
    AEDs_y = [AED[1] for AED in AED_positions]
    plt.scatter(AEDs_x, AEDs_y, color='red', marker='x', label="AED", s=100)

    plt.title(f"SNR Heatmap with {N}x{N} AP Grid")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    N = 4
    AP_positions = generate_APs(N)
    AU_position = np.array([0.7, 0.3, 0])
    AED_positions = [np.array([0.3, 0.3, 0]), np.array([0.7, 0.7, 0]), np.array([0.3, 0.7, 0])]
    
    # Generate passive eavesdropper sampled positions
    PED_positions = generate_sampled_positions()
    plot_PEDs(PED_positions)

    # Compute optimized beamforming vector
    w = compute_beamforming_vector(AP_positions, AU_position, AED_positions, PED_positions)
    print(f"Optimized Beamforming Vector: {w}")

    # Plot results
    plot_snr(N, AP_positions, w, AU_position, AED_positions)
