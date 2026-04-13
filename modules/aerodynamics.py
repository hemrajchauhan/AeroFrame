# modules/aerodynamics.py

from core.models import (
    Wing,
    FlightCondition,
    AerodynamicCoefficients,
    AerodynamicPerformance,
    AerodynamicState,
)

from utils.numerics import (
    compute_lift_coefficient,
    compute_induced_drag,
)


class Aerodynamics:
    """
    Computes aerodynamic characteristics of a wing.
    """

    def __init__(
        self,
        parasite_drag_coefficient: float = 0.02,
        oswald_efficiency: float = 0.8,
    ):
        self.parasite_drag_coefficient = parasite_drag_coefficient
        self.oswald_efficiency = oswald_efficiency

    # ============================================================
    # PUBLIC API
    # ============================================================

    def evaluate(
        self,
        wing: Wing,
        flight_condition: FlightCondition,
    ) -> AerodynamicState:
        """
        Compute aerodynamic state.

        Args:
            wing: Wing with geometry populated
            flight_condition: Flight condition

        Returns:
            AerodynamicState
        """

        self._validate_inputs(wing, flight_condition)

        # --- Lift ---
        lift_coefficient = compute_lift_coefficient(
            flight_condition.angle_of_attack
        )

        # --- Induced drag ---
        induced_drag = compute_induced_drag(
            lift_coefficient,
            wing.aspect_ratio,
            self.oswald_efficiency,
        )

        # --- Parasite drag ---
        parasite_drag = self.parasite_drag_coefficient

        # --- Total drag ---
        drag_coefficient = induced_drag + parasite_drag

        # --- Performance ---
        lift_to_drag = self._compute_lift_to_drag(
            lift_coefficient, drag_coefficient
        )

        coefficients = AerodynamicCoefficients(
            lift_coefficient=lift_coefficient,
            drag_coefficient=drag_coefficient,
            induced_drag_coefficient=induced_drag,
            parasite_drag_coefficient=parasite_drag,
        )

        performance = AerodynamicPerformance(
            lift_to_drag_ratio=lift_to_drag
        )

        return AerodynamicState(
            coefficients=coefficients,
            performance=performance,
        )

    # ============================================================
    # INTERNAL HELPERS
    # ============================================================

    def _validate_inputs(
        self,
        wing: Wing,
        flight_condition: FlightCondition,
    ) -> None:
        """
        Validate inputs to prevent non-physical calculations.
        """

        if wing.area <= 0.0:
            raise ValueError("Wing area must be positive.")

        if wing.span <= 0.0:
            raise ValueError("Wing span must be positive.")

        if self.oswald_efficiency <= 0.0:
            raise ValueError("Oswald efficiency must be positive.")

        if self.parasite_drag_coefficient < 0.0:
            raise ValueError("Parasite drag coefficient cannot be negative.")

    def _compute_lift_to_drag(
        self,
        lift_coefficient: float,
        drag_coefficient: float,
    ) -> float:
        """
        Safe computation of L/D ratio.
        """

        if drag_coefficient <= 0.0:
            raise ValueError("Drag coefficient must be positive.")

        return lift_coefficient / drag_coefficient
