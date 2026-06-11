import math

from src.models import Panel


def is_close(a: float, b: float, tolerance: float = 1e-5) -> bool:
    """Checks if two float values are practically equal within a tolerance."""
    return math.isclose(a, b, abs_tol=tolerance)


def is_rafter_crossing_panel(rafter_x: float, panel: Panel, clearance: float = 0.0) -> bool:
    """
    Checks if a vertical rafter line at x crosses the panel horizontal bounds,
    optionally keeping a safety clearance distance from the left and right edges.
    """
    # Rafter crosses if x is in range [left + clearance, right - clearance]
    return (panel.left + clearance) <= rafter_x <= (panel.right - clearance)