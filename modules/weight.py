# modules/weight.py

from dataclasses import dataclass
from core.models import Aircraft, WeightState


# ============================================================
# CONFIGURATION
# ============================================================

@dataclass
class WeightModelConfig:
    """
    Configuration parameters for weight estimation.

    All units in kg.
    """
    reference_weight: float = 70000.0
    empty_weight_fraction: float = 0.45
    fuel_weight_fraction: float = 0.30
    payload_weight: float = 18000.0


# ============================================================
# WEIGHT MODULE
# ============================================================

class WeightEstimation:
    """
    Simple parametric weight estimation model.
    """

    def __init__(self, config: WeightModelConfig = None):
        self.config = config or WeightModelConfig()

    # ============================================================
    # PUBLIC API
    # ============================================================

    def evaluate(self, aircraft: Aircraft) -> WeightState:
        """
        Compute aircraft weight breakdown.

        Args:
            aircraft: Aircraft model (not heavily used yet)

        Returns:
            WeightState
        """

        self._validate_config()

        empty_weight, fuel_weight, payload_weight = self._compute_weights()

        total_weight = empty_weight + fuel_weight + payload_weight

        self._validate_results(
            empty_weight,
            fuel_weight,
            payload_weight,
            total_weight,
        )

        return WeightState(
            empty_weight=empty_weight,
            payload_weight=payload_weight,
            fuel_weight=fuel_weight,
            total_weight=total_weight,
        )

    # ============================================================
    # INTERNAL HELPERS
    # ============================================================

    def _compute_weights(self) -> tuple:
        """
        Compute weight components using parametric model.
        """
        cfg = self.config

        empty_weight = cfg.empty_weight_fraction * cfg.reference_weight
        fuel_weight = cfg.fuel_weight_fraction * cfg.reference_weight
        payload_weight = cfg.payload_weight

        return empty_weight, fuel_weight, payload_weight

    def _validate_config(self) -> None:
        """
        Validate configuration inputs.
        """

        cfg = self.config

        if cfg.reference_weight <= 0.0:
            raise ValueError("Reference weight must be positive.")

        if not (0.0 < cfg.empty_weight_fraction < 1.0):
            raise ValueError("Empty weight fraction must be between 0 and 1.")

        if not (0.0 < cfg.fuel_weight_fraction < 1.0):
            raise ValueError("Fuel weight fraction must be between 0 and 1.")

        if cfg.payload_weight < 0.0:
            raise ValueError("Payload weight cannot be negative.")

    def _validate_results(
        self,
        empty_weight: float,
        fuel_weight: float,
        payload_weight: float,
        total_weight: float,
    ) -> None:
        """
        Validate computed weight results.
        """

        if empty_weight <= 0.0:
            raise ValueError("Empty weight must be positive.")

        if fuel_weight < 0.0:
            raise ValueError("Fuel weight cannot be negative.")

        if payload_weight < 0.0:
            raise ValueError("Payload weight cannot be negative.")

        if total_weight <= empty_weight:
            raise ValueError(
                "Total weight must be greater than empty weight."
            )
