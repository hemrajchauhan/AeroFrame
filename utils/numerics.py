# utils/numerics.py

import numpy as np
from numba import njit


@njit
def compute_lift_coefficient(angle_of_attack: float) -> float:
    """
    Compute lift coefficient using thin airfoil theory.

    CL = 2*pi*alpha

    Notes:
        - angle_of_attack must be in radians
        - no stall model included
    """

    # Basic sanity (Numba-safe)
    if not np.isfinite(angle_of_attack):
        return 0.0

    return 2.0 * np.pi * angle_of_attack


@njit
def compute_induced_drag(
    lift_coefficient: float,
    aspect_ratio: float,
    oswald_efficiency: float,
) -> float:
    """
    Compute induced drag coefficient.

    Cdi = CL^2 / (pi * AR * e)
    """

    # Guard against invalid inputs (Numba-safe)
    if aspect_ratio <= 0.0:
        return 0.0

    if oswald_efficiency <= 0.0:
        return 0.0

    if not np.isfinite(lift_coefficient):
        return 0.0

    denominator = np.pi * aspect_ratio * oswald_efficiency

    if denominator <= 0.0:
        return 0.0

    return (lift_coefficient ** 2) / denominator
