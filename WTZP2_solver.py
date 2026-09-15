"""Independent P0 solver for the one-dimensional WTZP2 pilot.

The code assembles the full Dirichlet form on (0, 1), including the exact
exterior confinement integral. It is intended for verification, not as a
high-order discretization of the continuum problem.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
from scipy.linalg import eigh


def cell_pair_weight(i: int, j: int, n: int, order: float) -> float:
    """Integral over two distinct uniform cells of |x-y|^(-1-order)."""
    if i > j:
        i, j = j, i
    if i == j:
        raise ValueError("P0 differences vanish on a diagonal cell")
    h = 1.0 / n
    a, b = i * h, (i + 1) * h
    c, d = j * h, (j + 1) * h
    q = 1.0 - order
    if abs(q) < 1e-10:
        # Continuous order -> 1 limit of the expression below.
        values = [d - b, c - a, c - b, d - a]
        return (np.log(values[0]) + np.log(values[1])
                - np.log(values[2]) - np.log(values[3])) / order
    numerator = (d - b) ** q + (c - a) ** q - (c - b) ** q - (d - a) ** q
    return numerator / (order * q)


def exterior_cell_weight(i: int, n: int, order: float) -> float:
    """Twice the exact exterior-tail integral over one cell."""
    h = 1.0 / n
    a, b = i * h, (i + 1) * h
    q = 1.0 - order
    if abs(q) < 1e-10:
        left = np.log(b) - (np.log(a) if a else 0.0)
        right = np.log(1.0 - a) - (np.log(1.0 - b) if b < 1 else 0.0)
        return 2.0 * (left + right) / order
    left = (b ** q - a ** q) / q
    right = ((1.0 - a) ** q - (1.0 - b) ** q) / q
    return 2.0 * (left + right) / order


def stiffness(beta: np.ndarray) -> np.ndarray:
    n = beta.size
    matrix = np.zeros((n, n), dtype=float)
    for i in range(n):
        matrix[i, i] += exterior_cell_weight(i, n, float(beta[i]))
        for j in range(i + 1, n):
            order = 0.5 * float(beta[i] + beta[j])
            # The full double integral contains both cell orientations.
            weight = 2.0 * cell_pair_weight(i, j, n, order)
            matrix[i, i] += weight
            matrix[j, j] += weight
            matrix[i, j] -= weight
            matrix[j, i] -= weight
    return matrix


def first_eigenpair(beta: np.ndarray) -> tuple[float, np.ndarray]:
    n = beta.size
    values, vectors = eigh(stiffness(beta), subset_by_index=[0, 0])
    vector = vectors[:, 0] / np.sqrt(1.0 / n)
    return float(values[0] * n), vector


def periodic_profile(n_cells: int, periods: int, theta: float,
                     beta_soft: float, beta_hard: float,
                     centered: bool = False) -> np.ndarray:
    x = (np.arange(n_cells) + 0.5) / n_cells
    phase = np.mod(periods * x, 1.0)
    if centered:
        soft = np.abs(phase - 0.5) < theta / 2.0
    else:
        soft = phase < theta
    return np.where(soft, beta_soft, beta_hard)


def run_joint_limit(output: Path, max_periods: int, cells_per_period: int) -> None:
    beta_soft, beta_hard, theta = 0.3, 0.7, 0.3
    rows = []
    periods = 1
    while periods <= max_periods:
        n = periods * cells_per_period
        mixed = periodic_profile(n, periods, theta, beta_soft, beta_hard)
        arithmetic = np.full(n, theta * beta_soft + (1.0 - theta) * beta_hard)
        heterogeneous, _ = first_eigenpair(mixed)
        relaxed, _ = first_eigenpair(arithmetic)
        rows.append((periods, n, relaxed, heterogeneous, heterogeneous - relaxed))
        print(f"n={periods:4d} N={n:5d} gap={heterogeneous-relaxed:+.8f}")
        periods *= 2
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["periods", "cells", "mu_arithmetic", "mu_two_phase", "gap"])
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-periods", type=int, default=8)
    parser.add_argument("--cells-per-period", type=int, default=40)
    parser.add_argument("--output", type=Path, default=Path("WTZP2_solver_joint_limit.csv"))
    args = parser.parse_args()
    run_joint_limit(args.output, args.max_periods, args.cells_per_period)


if __name__ == "__main__":
    main()
