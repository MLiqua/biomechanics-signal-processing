# biomechanics-signal-processing
A Python toolkit for analyzing FSR force-time data, filtering signals, and detecting gait events (heel strike & toe-off).

# WHAT IT DOES & WHY IT MATTERS
This project implements a complete force-signal processing pipeline for gait biomechanics. 
It loads FSR force-time data from CSV, applies smoothing filters (Moving Average, Butterworth), 
computes slopes, and automatically detects heel strike and toe-off events. 

This mirrors standard practice used in biomechanics research labs and wearable robotics systems.

 ## FEATURES
- Load time-series FSR force data from CSV
- Visualize raw force-time curves
- Compute slope (rate of force development)
- Moving Average smoothing
- 4th-order Butterworth low-pass filtering
- Heel strike and toe-off detection
- Plotting filtered vs raw force signals

# REPO STRUCTURE
biomechanics-signal-processing/
│
├── CSVdata/
│   └── fsr.csv
|
├── src/
│   └── force_signal_analysis.py
|
├── plots/
├── README.md
├── requirements.txt
└── .gitignore

# GENERATED GRAPHICS
### Raw
![Raw vs Filtered](plots/raw_force_data.png)



# LICENSE
This project is licensed under the MIT License.
