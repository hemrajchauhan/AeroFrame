# modules/performance.py

import numpy as np
from dataclasses import dataclass

from core.models import (
    AerodynamicState,
    WeightState,
    FlightCondition,
    PerformanceState,
)


# ============================================================
# CONFIGURATION
# ============================================================

@dataclass
class PerformanceConfig:
    """
    Configuration for performance calculations.

    Units:
        specific_fuel_consumption: 1/s
    """
    specific_fuel_consumption: float = 0.6 / 3600.0  # ~0.6 1/hr


# ============================================================
# PERFORMANCE MODULE
# ============================================================

class Performance:
    """
    Aircraft performance evaluation (range).
    """

    def __init__(self, config: PerformanceConfig = None):
        self.config = config or PerformanceConfig()

    # ============================================================
    # PUBLIC API
    # ============================================================

    def evaluate(
        self,
        aero: AerodynamicState,
        weight: WeightState,
        flight: FlightCondition,
    ) -> PerformanceState:
        """
        Compute aircraft range using Breguet equation.
        """

        self._validate_inputs(aero, weight, flight)

        range_m = self._compute_breguet_range(aero, weight, flight)

        return PerformanceState(range=range_m)

    # ============================================================
    # INTERNAL HELPERS
    # ============================================================

    def _validate_inputs(
        self,
        aero: AerodynamicState,
        weight: WeightState,
        flight: FlightCondition,
    ) -> None:
        """
        Validate inputs to ensure physically meaningful computation.
        """

        if flight.velocity <= 0.0:
            raise ValueError("Flight velocity must be positive.")

        if self.config.specific_fuel_consumption <= 0.0:
            raise ValueError("Specific fuel consumption must be positive.")

        if aero.performance.lift_to_drag_ratio <= 0.0:
            raise ValueError("Lift-to-drag ratio must be positive.")

        if weight.total_weight <= 0.0:
            raise ValueError("Total weight must be positive.")

        final_weight = weight.empty_weight + weight.payload_weight

        if final_weight <= 0.0:
            raise ValueError("Final weight must be positive.")

        if weight.total_weight <= final_weight:
            raise ValueError(
                "Initial weight must be greater than final weight for fuel burn."
            )

    def _compute_breguet_range(
        self,
        aero: AerodynamicState,
        weight: WeightState,
        flight: FlightCondition,
    ) -> float:
        """
        Compute range using Breguet equation.
        """

        V = flight.velocity
        c = self.config.specific_fuel_consumption
        L_over_D = aero.performance.lift_to_drag_ratio

        Wi = weight.total_weight
        Wf = weight.empty_weight + weight.payload_weight

        # Safe logarithm
        weight_ratio = Wi / Wf

        if weight_ratio <= 1.0:
            raise ValueError("Weight ratio must be greater than 1.")

        return (V / c) * L_over_D * np.log(weight_ratio)
