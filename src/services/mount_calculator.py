from config.settings import Settings
from src.models import Segment, Mount, Point
from src.services.interfaces import MountCalculatorInterface
from src.utils.exceptions import InfeasibleLayoutError
from src.utils.geometry import is_rafter_crossing_panel


class MountCalculator(MountCalculatorInterface):
    """
    Stateless calculator for mounts on rafters.
    """
    def __init__(self, settings: Settings):
        self.settings = settings

    def calculate_mounts(self, segments: list[Segment]) -> list[Mount]:
        """
        Calculates all valid mounts for the given segments.
        Raises InfeasibleLayoutError if layout cannot be supported.
        """
        mounts: list[Mount] = []

        for segment in segments:
            rafters = self._generate_crossing_rafters(segment.x_start, segment.x_end)
            valid_x_coordinates: list[float] = []
            
            for rafter_x in rafters:
                for panel in segment.panels:
                    if is_rafter_crossing_panel(rafter_x, panel, self.settings.mount.edge_clearance):
                        valid_x_coordinates.append(rafter_x)
                        break

            self._validate_feasibility(segment, valid_x_coordinates)
            y_levels = [segment.y, segment.y + self.settings.panel.height]

            for y in y_levels:
                for x in valid_x_coordinates:
                    mounts.append(Mount(position=Point(x, y)))

        return mounts

    def _generate_crossing_rafters(self, x_start: float, x_end: float) -> list[float]:
        """Generates all rafter x-coordinates within a horizontal range."""
        spacing = self.settings.rafter.spacing
        first_x = self.settings.rafter.first_rafter_x

        k_start = int((x_start - first_x) // spacing)
        k_end = int((x_end - first_x) // spacing) + 1

        rafters = []
        for k in range(k_start, k_end + 1):
            rafter_x = first_x + k * spacing
            if x_start <= rafter_x <= x_end:
                rafters.append(rafter_x)
        return rafters

    def _validate_feasibility(self, segment: Segment, supports: list[float]) -> None:
        """Enforces physical constraints. Raises InfeasibleLayoutError on violation."""
        if not supports:
            raise InfeasibleLayoutError(
                f"No valid rafters found crossing the segment at y={segment.y}."
            )

        left_cantilever = supports[0] - segment.x_start
        right_cantilever = segment.x_end - supports[-1]

        if left_cantilever > self.settings.mount.cantilever_limit:
            raise InfeasibleLayoutError(
                f"Left cantilever limit exceeded: {left_cantilever:.3f} > {self.settings.mount.cantilever_limit} "
                f"at y={segment.y}."
            )

        if right_cantilever > self.settings.mount.cantilever_limit:
            raise InfeasibleLayoutError(
                f"Right cantilever limit exceeded: {right_cantilever:.3f} > {self.settings.mount.cantilever_limit} "
                f"at y={segment.y}."
            )

        for i in range(len(supports) - 1):
            span = supports[i + 1] - supports[i]
            if span > self.settings.mount.span_limit:
                raise InfeasibleLayoutError(
                    f"Span limit exceeded: {span:.3f} > {self.settings.mount.span_limit} "
                    f"between consecutive supports at x={supports[i]:.3f} and x={supports[i+1]:.3f}."
                )