# Steel-Anisotropy-Digital-Twin

A physics-informed Digital Twin for simulating directional yield strength in high-performance steel using the Hill 1948 criterion.

Modeling Directional Yield Strength in High-Performance SteelThis project implements a physics-informed Digital Twin to simulate how yield strength varies with orientation in rolled steel variants. Using the Hill 1948 Anisotropy Criterion, the platform predicts the "M-curve" behavior of high-strength alloys.

**🛠 Key Features**

Automated Specimen Selection: Automatically identifies extreme high-strength and low-strength variants from the Ovako 100Cr6 dataset (https://steelnavigator.ovako.com/steel-grades/100cr6/).

High-Resolution Simulation: Executes a 181-degree angular sweep to predict directional performance.

Quantified Validation: Calculates absolute strength deltas and performance ratios at critical transverse points (90°).

**🧪 The Physics (Hill 1948)**

Unlike standard isotropic models taught in introductory mechanics, this engine accounts for directional texture using Lankford coefficients ($r_0$, $r_{45}$, $r_{90}$). 

The yield ratio is calculated using the Hill 1948 quadratic yield criterion:

$$ratio = \sqrt{F \sin^4 \theta + G \cos^4 \theta + H (\cos^2 \theta - \sin^2 \theta)^2 + 2N \sin^2 \theta \cos^2 \theta}$$

Where $\theta$ represents the angle relative to the rolling direction.

**📊 Results**

The simulation revealed a massive 1660.39 MPa gap between the strongest and weakest specimens at the 90° transverse point, with a performance ratio of 4.88x.
