import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import null_space
from APpositions import generate_APs, plot_APs

### PHYSICAL CONSTANTS (taken from section 5 of the paper)
phi_half = 60  # Half illuminance angle in degrees
m = -np.log(2) / np.log(np.cos(np.radians(phi_half)))  # Lambertian emission
IDC = 1  # Illumination DC current
eta = 1  # Current-to-light conversion efficiency (W/A)
R = 1  # Photodetector responsivity (A/W)
T = 1  # Transimpedance gain (V/A)
A_PD = 1  # Photodiode physical area (m^2)
sigma2 = math.pow(10, -9.833) # Noise power

def channel_gain(tx, rx):
    """
    Compute LoS channel gain transmitter i and receiver k.
    """
    tx_normal = np.array([0, 0, -1])
    rx_normal = np.array([0, 0, +1])
    
    # Compute the vector from transmitter to receiver
    tx_to_rx = np.array(rx) - np.array(tx)
    distance = np.linalg.norm(tx_to_rx)
    
    # Normalize the vectors
    tx_to_rx_normalized = tx_to_rx / distance
    tx_normal_normalized = tx_normal / np.linalg.norm(tx_normal)
    rx_normal_normalized = rx_normal / np.linalg.norm(rx_normal)
    
    # Compute the angle of irradiance (phi) and angle of incidence (psi)
    cos_phi = np.dot(tx_normal_normalized, tx_to_rx_normalized)
    cos_psi = np.dot(rx_normal_normalized, -tx_to_rx_normalized)
    
    return cos_phi * cos_psi

def compute_null_space(AP_positions, AED_position):
    """Compute a basis for the null space of the AED's channel vector."""
    H_AED = np.array([channel_gain(AP, AED_position) for AP in AP_positions]).reshape(-1, 1)
    return null_space(H_AED.T)  # Basis vectors for null space

def compute_snr(x, y, AP_positions, w):
    """Compute SNR at a given (x, y) point on the floor."""
    rx_position = np.array([x, y, 0])  # Floor level
    h_k = np.array([channel_gain(AP, rx_position) for AP in AP_positions])
    snr = (IDC**2 * (w.T @ h_k) ** 2) / sigma2
    return snr

def compute_beamforming_vector(AP_positions, AU_position, AED_position):
    """Compute the optimal beamforming vector w."""
    null_basis = compute_null_space(AP_positions, AED_position)
    w = null_basis[:, 0]  # Take the first basis vector (IMPORTANT: every base will zero SNR at AED, we need the one that maximizes SNR at the AU)
    h_AU = np.array([channel_gain(AP, AU_position) for AP in AP_positions])

    # Project h_AU onto the null space basis
    w_opt = null_basis @ (null_basis.T @ h_AU)
    return w_opt / np.linalg.norm(w_opt) # Normalize w

def plot_snr(N, AP_positions, w, AU_position, AED_position):
    """Plot the SNR heatmap with AU and AED positions."""
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
    
    # Plot only UE and AED positions
    plt.scatter(*AU_position[:2], color='yellow', marker='o', label="AU", s=100)
    plt.scatter(*AED_position[:2], color='red', marker='x', label="AED", s=100)

    plt.title(f"SNR Heatmap with {N}x{N} AP Grid")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    N = 16
    AP_positions = generate_APs(N)
    AU_position = np.array([0.5, 0.5, 0])  # Center of the grid
    AED_position = np.array([0.3, 0.3, 0])  # AED position

    # Compute beamforming vector
    w = compute_beamforming_vector(AP_positions, AU_position, AED_position)
    w = w/np.linalg.norm(w)
    print(f"Beamforming vector = {w}")

    # Plot SNR distribution
    plot_snr(N, AP_positions, w, AU_position, AED_position)
