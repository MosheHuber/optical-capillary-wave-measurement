"""
CapillaryWavesCameraFOV_RangeH_V1.py
-------------------------------------
Computes camera field-of-view (FOV) and horizontal pixel resolution as a
function of camera height above the water surface.

All results are reported in mm (or degrees for angular quantities).
Internal geometry calculations remain in metres.

Usage
-----
    python CapillaryWavesCameraFOV_RangeH_V1.py
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
h2 = np.arange(0, 3.01, 0.01)  # [m]  camera height above deck (swept variable)
h1 = 1.0                         # [m]  deck height above water surface
d1 = 0.0                         # [m]  camera horizontal distance inboard from railing
d2 = 2.0                         # [m]  shortest horizontal distance from ship to ROI
W  = 0.5                         # [m]  radial width of the region of interest (ROI)

Nx = 4096 // 2                   # [pixels]  horizontal pixel count

# ---------------------------------------------------------------------------
# Derived geometry  (internal calculations in metres)
# ---------------------------------------------------------------------------
z      = h1 + h2                                        # [m]  total camera height above water
x_near = d1 + d2                                        # [m]  distance to near edge of ROI
x_far  = x_near + W                                     # [m]  distance to far  edge of ROI

phi_far  = np.degrees(np.arctan(z / x_far))             # [deg]  depression angle to far  edge
phi_near = np.degrees(np.arctan(z / x_near))            # [deg]  depression angle to near edge
FOV      = phi_near - phi_far                           # [deg]  total angular FOV subtended by ROI

# ---------------------------------------------------------------------------
# Per-pixel horizontal resolution
# ---------------------------------------------------------------------------
nnx  = np.arange(1, Nx + 1)      # pixel index array 1 … Nx
resx = np.empty(len(FOV))        # [mm]  will hold mean pixel footprint for each h2

for n in range(len(FOV)):
    # Angular position of the centre of each pixel within the FOV
    phi  = phi_far[n] + (nnx - 0.5) * FOV[n] / Nx    # [deg]
    # Ground-plane distance corresponding to each pixel angle
    x_px = z[n] / np.tan(np.radians(phi))             # [m]
    # Mean pixel footprint → convert to mm
    resx[n] = np.mean(np.abs(np.diff(x_px))) * 1e3    # [mm]

# ---------------------------------------------------------------------------
# Results in mm / degrees
# ---------------------------------------------------------------------------
camera_height_mm = (h1 + h2) * 1e3   # [mm]  x-axis for plots

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Camera FOV vs Height above Water  |  RangeH", fontweight="bold")

axes[0].plot(camera_height_mm, FOV, color="steelblue", linewidth=1.8)
axes[0].set_xlabel("Camera height above water [mm]")
axes[0].set_ylabel("FOV [deg]")
axes[0].set_title("Field of View vs Camera Height")
axes[0].grid(True, linestyle="--", alpha=0.6)

axes[1].plot(camera_height_mm, resx, color="darkorange", linewidth=1.8)
axes[1].set_xlabel("Camera height above water [mm]")
axes[1].set_ylabel("Horizontal resolution [mm / pixel]")
axes[1].set_title("Pixel Resolution vs Camera Height")
axes[1].grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("CapillaryWavesCameraFOV_RangeH_V1.png", dpi=150)
plt.show()
print("Saved: CapillaryWavesCameraFOV_RangeH_V1.png")
