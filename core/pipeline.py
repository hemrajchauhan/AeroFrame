# core/pipeline.py

from core.models import (
    Aircraft,
    FlightCondition,
    AnalysisResult,
    WeightState,
)

from interfaces.cpacs import CPACSReader, CPACSAdapter
from geometry.tigl_geometry import GeometryService
from modules.aerodynamics import Aerodynamics
from modules.weight import WeightEstimation
from modules.performance import Performance, PerformanceConfig


class AeroFramePipeline:
    """
    Central orchestration of AeroFrame analysis.
    """

    def __init__(self, cpacs_path: str):
        self.cpacs_path = cpacs_path

    # ============================================================
    # PUBLIC API
    # ============================================================

    def run(self, flight_condition: FlightCondition = None) -> AnalysisResult:
        """
        Execute full aircraft analysis pipeline.

        Args:
            flight_condition: Optional override of CPACS flight condition

        Returns:
            AnalysisResult
        """

        # --------------------------------------------------------
        # 1. CPACS → Aircraft model
        # --------------------------------------------------------
        reader = CPACSReader(self.cpacs_path)
        adapter = CPACSAdapter(reader)

        aircraft = adapter.build_aircraft()

        # --------------------------------------------------------
        # 2. Geometry (TiGL)
        # --------------------------------------------------------
        geometry = GeometryService(reader.get_tixi_handle())

        enriched_wing = geometry.enrich_wing(aircraft.wing)

        aircraft = Aircraft(
            name=aircraft.name,
            wing=enriched_wing,
        )

        # --------------------------------------------------------
        # 3. READ CPACS CONFIG DATA
        # --------------------------------------------------------
        aero_cfg = reader.get_aerodynamics_config()
        weight_data = reader.get_weight_data()
        flight_data = reader.get_flight_condition_data()
        perf_cfg = reader.get_performance_config()

        # --------------------------------------------------------
        # 4. Flight Condition (CPACS or override)
        # --------------------------------------------------------
        if flight_condition is None:
            flight_condition = FlightCondition(
                velocity=flight_data["velocity"],
                air_density=flight_data["air_density"],
                angle_of_attack=flight_data["angle_of_attack"],
            )

        # --------------------------------------------------------
        # 5. Aerodynamics
        # --------------------------------------------------------
        aero_model = Aerodynamics(
            parasite_drag_coefficient=aero_cfg["parasite_drag_coefficient"],
            oswald_efficiency=aero_cfg["oswald_efficiency"],
        )

        aero_state = aero_model.evaluate(
            aircraft.wing,
            flight_condition,
        )

        # --------------------------------------------------------
        # 6. Weight (CPACS OR fallback)
        # --------------------------------------------------------
        if all(v is not None for v in weight_data.values()):
            empty = weight_data["empty_weight"]
            payload = weight_data["payload_weight"]
            fuel = weight_data["fuel_weight"]

            weight_state = WeightState(
                empty_weight=empty,
                payload_weight=payload,
                fuel_weight=fuel,
                total_weight=empty + payload + fuel,
            )
        else:
            # fallback to model
            weight_model = WeightEstimation()
            weight_state = weight_model.evaluate(aircraft)

        # --------------------------------------------------------
        # 7. Performance
        # --------------------------------------------------------
        performance_model = Performance(
            config=PerformanceConfig(
                specific_fuel_consumption=perf_cfg["specific_fuel_consumption"]
            )
        )

        performance_state = performance_model.evaluate(
            aero=aero_state,
            weight=weight_state,
            flight=flight_condition,
        )

        # --------------------------------------------------------
        # 8. Aggregate results
        # --------------------------------------------------------
        return AnalysisResult(
            aircraft=aircraft,
            aerodynamic_state=aero_state,
            weight_state=weight_state,
            performance_state=performance_state,
        )
