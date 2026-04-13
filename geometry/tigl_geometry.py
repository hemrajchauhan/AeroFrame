# geometry/tigl_geometry.py

from tigl3.tigl3wrapper import Tigl3
from core.models import Wing


class GeometryService:
    """
    Geometry extraction using TiGL.
    """

    def __init__(self, tixi_handle: int):
        self.tigl = Tigl3()
        self.tigl.openCPACSConfiguration(tixi_handle, "")

        # Cache UID → index mapping
        self._wing_uid_to_index = self._build_wing_index_map()

    # ============================================================
    # PUBLIC API
    # ============================================================

    def enrich_wing(self, wing: Wing) -> Wing:
        """
        Returns a new Wing object with geometry populated.
        """

        index = self._get_wing_index(wing.uid)

        span = self.tigl.wingGetSpan(wing.uid)
        area = self.tigl.wingGetSurfaceArea(index)

        return Wing(
            uid=wing.uid,
            span=span,
            area=area,
        )

    def get_all_wing_uids(self) -> list[str]:
        """
        Returns all wing UIDs from CPACS.
        """
        return list(self._wing_uid_to_index.keys())

    # ============================================================
    # INTERNAL HELPERS
    # ============================================================

    def _build_wing_index_map(self) -> dict:
        """
        Build UID → index mapping once (performance improvement).
        """
        mapping = {}

        n_wings = self.tigl.getWingCount()

        for i in range(1, n_wings + 1):
            uid = self.tigl.wingGetUID(i)
            mapping[uid] = i

        return mapping

    def _get_wing_index(self, uid: str) -> int:
        try:
            return self._wing_uid_to_index[uid]
        except KeyError:
            raise ValueError(f"Wing UID '{uid}' not found in CPACS.")
