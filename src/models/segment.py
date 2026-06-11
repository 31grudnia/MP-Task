from src.models.panel import Panel


class Segment:
    """Represents a continuous horizontal group of adjacent solar panels."""
    def __init__(self, panels: list[Panel]):
        if not panels:
            raise ValueError("A segment must contain at least one panel.")
        
        # sorting panels horizontally to ensure boundaries are correct
        self._panels = sorted(panels, key=lambda p: p.left)

    @property
    def panels(self) -> list[Panel]:
        """Returns the sorted list of panels in this segment."""
        return self._panels

    @property
    def x_start(self) -> float:
        """The leftmost coordinate of the entire continuous segment."""
        return self._panels[0].left

    @property
    def x_end(self) -> float:
        """The rightmost coordinate of the entire continuous segment."""
        return self._panels[-1].right

    @property
    def y(self) -> float:
        """The common row vertical coordinate of the segment."""
        return self._panels[0].top