# core/models.py

from dataclasses import dataclass
from typing import Optional


# ============================================================
# GEOMETRY MODELS
# ============================================================

@dataclass
class Wing:
    """
    Represents a lifting surface extracted from CPACS/TiGL.

    Units:
        area: m^2
        span: m
    """
    uid: str
    area: float
    span: float

    @property
    def aspect_ratio(self) -> float:
        """
        Aspect ratio AR = b^2 / S
        """
        if self.area <= 0.0:
            raise ValueError("Wing area must be positive to compute aspect ratio.")
        return self.span ** 2 / self.area


@dataclass
class Aircraft:
    """
    High-level aircraft model.

    For now, only a single wing is considered.
    """
    name: str
    wing: Wing


# ============================================================
# FLIGHT CONDITION
# ============================================================

@dataclass
class FlightCondition:
    """
    Defines the flight state.

    Units:
        velocity: m/s
        air_density: kg/m^3
        angle_of_attack: radians
        mach_number: [-]
    """
    velocity: float
    air_density: float
    angle_of_attack: float
    mach_number: Optional[float] = None


# ============================================================
# AERODYNAMICS
# ============================================================

@dataclass
class AerodynamicCoefficients:
    """
    Aerodynamic coefficients (dimensionless).
    """
    lift_coefficient: float
    drag_coefficient: float
    induced_drag_coefficient: float
    parasite_drag_coefficient: float


@dataclass
class AerodynamicPerformance:
    """
    Derived aerodynamic performance metrics.
    """
    lift_to_drag_ratio: float


@dataclass
class AerodynamicState:
    """
    Complete aerodynamic state output.
    """
    coefficients: AerodynamicCoefficients
    performance: AerodynamicPerformance


# ============================================================
# WEIGHT
# ============================================================

@dataclass
class WeightState:
    """
    Aircraft weight breakdown.

    Units:
        weights in kg
    """
    empty_weight: float
    payload_weight: float
    fuel_weight: float
    total_weight: float


# ============================================================
# PERFORMANCE
# ============================================================

@dataclass
class PerformanceState:
    """
    Aircraft performance outputs.

    Units:
        range: meters
    """
    range: float


# ============================================================
# AIRCRAFT ANALYSIS RESULT
# ============================================================


@dataclass
class AnalysisResult:
    """
    Aggregated result of full aircraft analysis.
    """
    aircraft: Aircraft
    aerodynamic_state: AerodynamicState
    weight_state: WeightState
    performance_state: PerformanceState