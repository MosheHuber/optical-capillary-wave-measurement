"""
SurfWavesDisp_CGtransition.py
-------------------------------
Computes and plots the gravity-capillary wave dispersion relation and the
ratio of capillary-to-gravity contributions over a range of wavelengths.

Results reported in mm (wavelength axis) and seconds (wave period).
The capillary-to-gravity ratio is dimensionless.
Internal physics calculations remain in SI (metres).

Usage
-----
    python SurfWavesDisp_CGtransition.py
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
g     = 9.8       # [m/s²]   gravitational acceleration
d     = 100.0     # [m]      ocean depth (for tanh finite-depth correction)
gamma = 0.074     # [N/m]    surface tension coefficient (air-water)
rho0  = 1000.0    # [kg/m³]  water density

# ---------------------------------------------------------------------------
# Wavelength range  (internal SI, results reported in mm)
# ---------------------------------------------------------------------------
WL = np.arange(0.001, 0.101, 0.001)   # [m]  1 mm … 100 mm

# ---------------------------------------------------------------------------
# Dispersion relation:  ω² = (g·k + γ/ρ · k³) · tanh(k·d)
# ---------------------------------------------------------------------------
k         = 2 * np.pi / WL                               # [rad/m]  wavenumber
omega_sq  = (g * k + (gamma / rho0) * k**3) * np.tanh(k * d)
omega     = np.sqrt(omega_sq)                            # [rad/s]

T         = 2 * np.pi / omega                            # [s]  wave period
f         = 1.0 / T                                      # [Hz] wave frequency

# Ratio of capillary to gravity contribution to the dispersion relation
# = (γ/ρ · k³) / (g · k)  = (γ/ρ · k²) / g
C2G_ratio = (gamma / rho0) * k**2 / g                   # [-]  dimensionless

# ---------------------------------------------------------------------------
# Diagnostic prints at the two key wavelengths
# ---------------------------------------------------------------------------
wl_markers = [0.017, 0.008]   # [m]  1.7 cm and 0.8 cm crossover wavelengths
print(f"{'WL [mm]':>10}  {'T [ms]':>10}  {'f [Hz]':>10}  {'C/G ratio':>12}")
print("-" * 48)
for wl_m in wl_markers:
    idx = np.argmin(np.abs(WL - wl_m))
    print(f"{WL[idx]*1e3:>10.1f}  {T[idx]*1e3:>10.2f}  "
          f"{f[idx]:>10.2f}  {C2G_ratio[idx]:>12.3f}")

# ---------------------------------------------------------------------------
# Results in mm (wavelength) and seconds (period)
# ---------------------------------------------------------------------------
WL_mm = WL * 1e3      # [mm]  for x-axis

fig, ax1 = plt.subplots(figsize=(9, 5))
fig.suptitle(
    "Surface wave dispersion relation\n"
    "(Left) Period vs Wavelength  |  (Right) Capillary / Gravity ratio",
    fontweight="bold"
)

# Left y-axis: wave period [s]
color_T = "steelblue"
ax1.set_xlabel("Wavelength [mm]")
ax1.set_ylabel("Period T [s]", color=color_T)
ax1.semilogx(WL_mm, T, color=color_T, linewidth=1.8, label="Period T [s]")
ax1.tick_params(axis="y", labelcolor=color_T)
ax1.grid(True, which="both", linestyle="--", alpha=0.5)

# Mark the two key wavelengths on period axis
for wl_m in wl_markers:
    idx = np.argmin(np.abs(WL - wl_m))
    ax1.axvline(WL_mm[idx], color="gray", linestyle=":", linewidth=1)
    ax1.annotate(
        f"λ={WL_mm[idx]:.1f} mm\nT={T[idx]*1e3:.1f} ms",
        xy=(WL_mm[idx], T[idx]),
        xytext=(WL_mm[idx] * 1.3, T[idx] * 1.4),
        fontsize=8,
        color="gray",
        arrowprops=dict(arrowstyle="->", color="gray", lw=0.8),
    )

# Right y-axis: capillary / gravity ratio (log scale)
ax2 = ax1.twinx()
color_R = "darkorange"
ax2.set_ylabel("Capillary / Gravity ratio  [–]", color=color_R)
ax2.loglog(WL_mm, C2G_ratio, color=color_R, linewidth=1.8,
           linestyle="--", label="C/G ratio")
ax2.axhline(1.0, color="dimgray", linestyle="-.", linewidth=1,
            label="C/G = 1 (crossover)")
ax2.tick_params(axis="y", labelcolor=color_R)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)

plt.tight_layout()
plt.savefig("SurfWavesDisp_CGtransition.png", dpi=150)
plt.show()
print("Saved: SurfWavesDisp_CGtransition.png")
