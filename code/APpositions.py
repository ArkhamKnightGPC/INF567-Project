import numpy as np
import matplotlib.pyplot as plt

def generate_APs(N):
    """Generate NxN Access Point positions inside 1x1 room."""
    points = []
    step = 1 / (N + 1)  # Step size, avoiding boundary points
    coords = np.linspace(step, 1 - step, N)  # N internal points

    for x in coords:
        for y in coords:
            points.append((x, y, 1))
    
    return points

def plot_APs(N):
    """Plot for the report!"""
    points = generate_APs(N)
    x_vals, y_vals, _ = zip(*points)  # Unpack points

    plt.figure(figsize=(5, 5))
    plt.scatter(x_vals, y_vals, color='blue', marker='o', label=f"AP")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect('equal', adjustable='box')

    # Draw grid lines
    step = 1 / (N + 1)
    for i in range(1, N + 1):
        plt.axhline(i * step, color='gray', linestyle='--', linewidth=0.5)
        plt.axvline(i * step, color='gray', linestyle='--', linewidth=0.5)

    plt.title(f"{N}x{N} Access Point grid")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    N = 16
    plot_APs(N)
