import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =====================
# Load Data
# =====================
df = pd.read_csv("data/results.csv")

# =====================
# Compute Accuracy
# =====================
summary = (
    df.groupby(["spatial_freq", "contrast"])
      .correct
      .mean()
      .reset_index()
)

# =====================
# Estimate Thresholds
# (closest contrast to 75% correct)
# =====================
thresholds = []

for sf in summary.spatial_freq.unique():
    sf_data = summary[summary.spatial_freq == sf]
    sf_data = sf_data.sort_values("contrast")

    # Find contrast closest to 75% correct
    sf_data["distance"] = np.abs(sf_data.correct - 0.75)
    threshold = sf_data.loc[sf_data.distance.idxmin()].contrast

    thresholds.append({
        "spatial_freq": sf,
        "threshold": threshold,
        "sensitivity": 1 / threshold
    })

thresholds = pd.DataFrame(thresholds)

# =====================
# Plot CSF
# =====================
plt.figure(figsize=(7, 5))
plt.plot(
    thresholds.spatial_freq,
    thresholds.sensitivity,
    marker="o"
)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Spatial Frequency (cycles/degree)")
plt.ylabel("Contrast Sensitivity (1 / threshold)")
plt.title("Contrast Sensitivity Function (CSF)")
plt.grid(True)

plt.show()