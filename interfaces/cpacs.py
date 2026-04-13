# interfaces/cpacs.py

from tixi3wrapper import Tixi3
from typing import Optional, Dict
from core.models import Aircraft, Wing


# ============================================================
# LOW-LEVEL READER (TiXI WRAPPER)
# ============================================================

class CPACSReader:
    """
    Thin wrapper around TiXI for CPACS access.
    Responsible ONLY for reading raw CPACS data.
    """

    def __init__(self, file_path: str):
        self.tixi = Tixi3()
        self.tixi.open(file_path)

    # ============================================================
    # BASIC ACCESSORS
    # ============================================================

    def get_aircraft_name(self) -> str:
        return self.tixi.getTextElement("/cpacs/header/name")

    def get_wing_uid(self, index: int = 1) -> str:
        xpath = f"/cpacs/vehicles/aircraft/model/wings/wing[{index}]"
        return self.tixi.getTextAttribute(xpath, "uID")

    # ============================================================
    # GENERIC SAFE ACCESS
    # ============================================================

    def _get_float(self, xpath: str, default: Optional[float] = None) -> Optional[float]:
        try:
            return self.tixi.getDoubleElement(xpath)
        except Exception:
            return default

    def _get_text(self, xpath: str, default: Optional[str] = None) -> Optional[str]:
        try:
            return self.tixi.getTextElement(xpath)
        except Exception:
            return default

    # ============================================================
    # AEROFRAME DATA (TOOLSPECIFIC)
    # ============================================================

    def get_aerodynamics_config(self) -> Dict[str, float]:
        base = "/cpacs/vehicles/aircraft/model/toolspecific/aeroFrame/aerodynamics"

        return {
            "parasite_drag_coefficient": self._get_float(
                f"{base}/parasiteDragCoefficient", 0.02
            ),
            "oswald_efficiency": self._get_float(
                f"{base}/oswaldEfficiency", 0.8
            ),
        }

    def get_weight_data(self) -> Dict[str, Optional[float]]:
        base = "/cpacs/vehicles/aircraft/model/toolspecific/aeroFrame/weight"

        return {
            "empty_weight": self._get_float(f"{base}/emptyWeight"),
            "payload_weight": self._get_float(f"{base}/payloadWeight"),
            "fuel_weight": self._get_float(f"{base}/fuelWeight"),
        }

    def get_flight_condition_data(self) -> Dict[str, Optional[float]]:
        base = "/cpacs/vehicles/aircraft/model/toolspecific/aeroFrame/flightCondition"

        return {
            "velocity": self._get_float(f"{base}/velocity"),
            "air_density": self._get_float(f"{base}/airDensity"),
            "angle_of_attack": self._get_float(f"{base}/angleOfAttack"),
        }

    def get_performance_config(self) -> Dict[str, float]:
        base = "/cpacs/vehicles/aircraft/model/toolspecific/aeroFrame/performance"

        return {
            "specific_fuel_consumption": self._get_float(
                f"{base}/specificFuelConsumption", 0.0001667
            ),
        }

    # ============================================================
    # UTILITY
    # ============================================================

    def get_tixi_handle(self) -> int:
        return self.tixi._handle.value

    def close(self):
        self.tixi.close()


# ============================================================
# ADAPTER (CPACS → CORE MODELS)
# ============================================================

class CPACSAdapter:
    """
    Converts CPACS data into AeroFrame core models.
    """

    def __init__(self, reader: CPACSReader):
        self.reader = reader

    def build_aircraft(self) -> Aircraft:
        name = self.reader.get_aircraft_name()
        wing_uid = self.reader.get_wing_uid()

        wing = Wing(
            uid=wing_uid,
            area=0.0,
            span=0.0,
        )

        return Aircraft(
            name=name,
            wing=wing,
        )
