"""
Biomechanics signal processing demo:
- Load FSR data
- Filter using Moving Average & Butterworth
- Detect heel strike & toe-off
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# ---------------------- Functions ---------------------- #

# Ensures CSV loading works regardless of VS Code workspace.
def set_working_directory_to_script():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print("Working directory:", os.getcwd())

# Import time and force columns from an FSR CSV file. 
def load_fsr_csv(filename: str):
    data = pd.read_csv(filename, encoding="utf-8-sig")
    data.columns = data.columns.str.strip()
    time = data["time"].to_numpy()
    force = data["force"].to_numpy()
    return time, force

# Estimate sampling frequency (Hz) from time array.
def compute_sampling_rate(time: np.ndarray) -> float:
    dt = np.mean(np.diff(time))
    fs = 1.0 / dt
    return fs

# Simple moving average filter.
def moving_average(signal: np.ndarray, window: int = 3) -> np.ndarray:
    kernel = np.ones(window) / window
    return np.convolve(signal, kernel, mode="same")
 
"""   
Apply a zero-phase Butterworth low-pass filter.
    fs : sampling frequency (Hz)
    fc : cutoff frequency (Hz), must be < fs/2
    order : Butterworth filter order
"""
def butterworth_lowpass(signal: np.ndarray,
                        fs: float,
                        fc: float = 8.0,
                        order: int = 4) -> np.ndarray:
    nyquist = fs / 2.0
    fc_clipped = min(fc, 0.99 * nyquist)  # safety: keep below Nyquist
    Wn = fc_clipped / nyquist

    b, a = butter(order, Wn, btype="low")
    filtered = filtfilt(b, a, signal)
    return filtered

"""
Detect heel strike (max positive slope) and toe-off (max negative slope) in a force signal.
    Returns: heel_idx, toe_idx, heel_time, toe_time
"""
def detect_heel_toe(force: np.ndarray, time: np.ndarray):
    slope = np.diff(force)
    heel_idx = int(np.argmax(slope))
    toe_idx = int(np.argmin(slope))

    heel_time = time[heel_idx + 1]
    toe_time = time[toe_idx + 1]

    return heel_idx + 1, toe_idx + 1, heel_time, toe_time

# --------------------------- Main --------------------------- #
def main():
    set_working_directory_to_script()

    # Load data
    time, force = load_fsr_csv("fsr.csv")
    fs = compute_sampling_rate(time)
    print(f"Estimated sampling rate: {fs:.2f} Hz")

    # Basic plots: raw force
    plt.figure()
    plt.plot(time, force)
    plt.xlabel("Time (s)")
    plt.ylabel("Force (N)")
    plt.title("Raw Force Data")
    plt.tight_layout()
    plt.show()

    # Slope (rate of change) of raw force
    slope_raw = np.diff(force)
    plt.figure()
    plt.plot(time[1:], slope_raw)
    plt.xlabel("Time (s)")
    plt.ylabel("Slope (N/s)")
    plt.title("Force Slope (Raw)")
    plt.tight_layout()
    plt.show()

    # Moving average smoothing
    ma_force = moving_average(force, window=3)
    plt.figure()
    plt.plot(time, force, label="Raw", alpha=0.6)
    plt.plot(time, ma_force, label="Moving Avg (3)", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Force (N)")
    plt.title("Moving Average Smoothing")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Butterworth low-pass smoothing
    butter_force = butterworth_lowpass(force, fs, fc=8.0, order=4)

    plt.figure()
    plt.plot(time, force, label="Raw", alpha=0.6)
    plt.plot(time, butter_force, label="Butterworth 8 Hz", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Force (N)")
    plt.title("Raw vs Butterworth-Filtered Force")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Event detection on filtered force
    heel_idx, toe_idx, heel_time, toe_time = detect_heel_toe(butter_force, time)
    print(f"Heel strike (filtered): t = {heel_time:.3f} s (index {heel_idx})")
    print(f"Toe-off (filtered):     t = {toe_time:.3f} s (index {toe_idx})")

    plt.figure()
    plt.plot(time, butter_force, label="Filtered Force")
    plt.scatter(heel_time, butter_force[heel_idx], color="green", label="Heel strike")
    plt.scatter(toe_time, butter_force[toe_idx], color="red", label="Toe-off")
    plt.xlabel("Time (s)")
    plt.ylabel("Force (N)")
    plt.title("Filtered Force with Heel Strike & Toe-Off")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()