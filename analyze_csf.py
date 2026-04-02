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
# Estimate Thresholds (Interpolated 75%)
# =====================
thresholds = []

for sf in sorted(summary.spatial_freq.unique()):
    sf_data = summary[summary.spatial_freq == sf]
    sf_data = sf_data.sort_values("contrast")

    contrasts = sf_data.contrast.values
    accuracy = sf_data.correct.values

    # Enforce monotonicity (prevents noisy dips)
    accuracy = np.maximum.accumulate(accuracy)

    # Check that curve crosses 75%
    if accuracy.min() <= 0.75 <= accuracy.max():
        threshold = np.interp(0.75, accuracy, contrasts)
    else:
        # If 75% not reached, use highest contrast as conservative threshold
        threshold = contrasts[-1]

    thresholds.append({
        "spatial_freq": sf,
        "threshold": threshold,
        "sensitivity": 1 / threshold
    })

thresholds = pd.DataFrame(thresholds)

# =====================
# Smooth CSF (across spatial frequency)
# =====================
log_sf = np.log10(thresholds.spatial_freq.values)
log_sens = np.log10(thresholds.sensitivity.values)

# Fit smooth curve (2nd order polynomial in log-log space)
coeffs = np.polyfit(log_sf, log_sens, deg=2)
sf_fit = np.logspace(log_sf.min(), log_sf.max(), 200)
sens_fit = 10 ** np.polyval(coeffs, np.log10(sf_fit))

# =====================
# Plot CSF
# =====================
plt.figure(figsize=(7, 5))

# Raw points
plt.scatter(
    thresholds.spatial_freq,
    thresholds.sensitivity,
    label="Estimated Sensitivity",
    zorder=2
)

# Smooth CSF curve
plt.plot(
    sf_fit,
    sens_fit,
    label="Smoothed CSF",
    linewidth=2,
    zorder=1
)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Spatial Frequency (cycles/degree)")
plt.ylabel("Contrast Sensitivity (1 / threshold)")
plt.title("Contrast Sensitivity Function (CSF)")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.5)

plt.show()