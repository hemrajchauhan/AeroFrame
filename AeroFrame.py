# AeroFrame.py

from utils.environment import setup_environment
setup_environment()

from core.pipeline import AeroFramePipeline
from core.models import FlightCondition


def main():
    cpacs_path = "data/aircraft.xml"

    pipeline = AeroFramePipeline(cpacs_path)

    # ------------------------------------------------------------
    # Fully CPACS-driven
    # ------------------------------------------------------------
    try:
        result = pipeline.run()
    except Exception as e:
        print("⚠️ CPACS missing data, using fallback flight condition")
        print("Reason:", e)

    # ------------------------------------------------------------
    # Output
    # ------------------------------------------------------------
    _print_results(result)


# ============================================================
# OUTPUT FORMATTER
# ============================================================

def _print_results(result):
    print("\n================ AeroFrame Results ================\n")

    print(f"Aircraft: {result.aircraft.name}")

    print("\n--- Geometry ---")
    print(f"Span: {result.aircraft.wing.span:.3f} m")
    print(f"Area: {result.aircraft.wing.area:.3f} m²")

    print("\n--- Aerodynamics ---")
    aero = result.aerodynamic_state.coefficients
    perf = result.aerodynamic_state.performance

    print(f"CL: {aero.lift_coefficient:.4f}")
    print(f"CD: {aero.drag_coefficient:.4f}")
    print(f"L/D: {perf.lift_to_drag_ratio:.2f}")

    print("\n--- Weight ---")
    w = result.weight_state
    print(f"Empty: {w.empty_weight:.1f} kg")
    print(f"Payload: {w.payload_weight:.1f} kg")
    print(f"Fuel: {w.fuel_weight:.1f} kg")
    print(f"Total: {w.total_weight:.1f} kg")

    print("\n--- Performance ---")
    print(f"Range: {result.performance_state.range / 1000:.2f} km")

    print("\n==================================================\n")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
