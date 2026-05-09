"""
CapillaryWavesCameraFOV_RangeD_V1.py
--------------------------------------
Computes camera field-of-view (FOV) and horizontal pixel resolution as a
function of the horizontal distance between the camera and the region of
interest (ROI) on the water surface.

All results are reported in mm (or degrees for angular quantities).
Internal geometry calculations remain in metres.

Usage
-----
    python CapillaryWavesCameraFOV_RangeD_V1.py
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
h2 = 1.0                                   # [m]  camera height above deck
h1 = 1.0                                   # [m]  deck height above water
d1 = 0.0                                   # [m]  camera horizontal distance inboard from railing
d2 = np.arange(1.0, 4.01, 0.01)            # [m]  distance from ship to ROI (swept variable)
W  = 0.5                                   # [m]  radial width of the ROI

Nx = 4096 // 2                             # [pixels]  horizontal pixel count

# ---------------------------------------------------------------------------
# Derived geometry  (internal calculations in metres)
# ---------------------------------------------------------------------------
z      = h1 + h2                                        # [m]  total camera height above water
x_near = d1 + d2                                        # [m]  distance to near edge of ROI
x_far  = x_near + W                                     # [m]  distance to far  edge of ROI

phi_far  = np.degrees(np.arctan(z / x_far))             # [deg]  depression angle to far  edge
phi_near = np.degrees(np.arctan(z / x_near))            # [deg]  depression angle to near edge
FOV      = phi_near - phi_far                           # [deg]  total angular FOV

# ---------------------------------------------------------------------------
# Per-pixel horizontal resolution
# ---------------------------------------------------------------------------
nnx  = np.arange(1, Nx + 1)      # pixel index array 1 … Nx
resx = np.empty(len(FOV))        # [mm]  mean pixel footprint for each d2 value

for n in range(len(FOV)):
    # Angular position of the centre of each pixel within the FOV
    phi  = phi_far[n] + (nnx - 0.5) * FOV[n] / Nx    # [deg]
    # Ground-plane distance corresponding to each pixel angle
    x_px = z / np.tan(np.radians(phi))                # [m]
    # Mean pixel footprint → convert to mm
    resx[n] = np.mean(np.abs(np.diff(x_px))) * 1e3    # [mm]

# ---------------------------------------------------------------------------
# Results in mm / degrees
# ---------------------------------------------------------------------------
d2_mm = d2 * 1e3    # [mm]  x-axis for plots

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Camera FOV vs ROI Distance  |  RangeD", fontweight="bold")

axes[0].plot(d2_mm, FOV, color="steelblue", linewidth=1.8)
axes[0].set_xlabel("ROI distance from camera [mm]")
axes[0].set_ylabel("FOV [deg]")
axes[0].set_title("Field of View vs ROI Distance")
axes[0].grid(True, linestyle="--", alpha=0.6)

axes[1].plot(d2_mm, resx, color="darkorange", linewidth=1.8)
axes[1].set_xlabel("ROI distance from camera [mm]")
axes[1].set_ylabel("Horizontal resolution [mm / pixel]")
axes[1].set_title("Pixel Resolution vs ROI Distance")
axes[1].grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("CapillaryWavesCameraFOV_RangeD_V1.png", dpi=150)
plt.show()
print("Saved: CapillaryWavesCameraFOV_RangeD_V1.png")
