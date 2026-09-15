# Reproducibility instructions

Requirements: Python 3.10+, NumPy, SciPy.

From this directory run:

```powershell
python WTZP2_reproduce_reported_tables.py
python WTZP2_solver.py --cells-per-period 67 --max-periods 16
```

The first command validates the archived reported tables. The second independently assembles the full one-dimensional Dirichlet form, including exterior confinement, and reproduces the first five joint-limit values displayed in the manuscript to its reported precision: 0.18000107, 0.79540680, 1.00083054, 1.09962095, and 1.15525313.

The larger archived resolutions are retained as source data but are intentionally not part of the default quick rerun because dense generalized eigenvalue solves become expensive. The solver is a verification-oriented P0 discretization, not a claimed high-order continuum solver.
