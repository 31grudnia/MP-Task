import pytest

from config.settings import Settings
from src.models import Point, Panel


@pytest.fixture
def default_settings() -> Settings:
    return Settings()


@pytest.fixture
def pdf_example_data() -> list[dict[str, float]]:
    """The exact panel coordinates"""
    return [
        {"x": 0, "y": 0}, {"x": 45.05, "y": 0}, {"x": 90.1, "y": 0},
        {"x": 0, "y": 71.6}, {"x": 135.15, "y": 0}, {"x": 135.15, "y": 71.6},
        {"x": 0, "y": 143.2}, {"x": 45.05, "y": 143.2}, {"x": 135.15, "y": 143.2},
        {"x": 90.1, "y": 143.2}
    ]


@pytest.fixture
def impossible_roof_data() -> list[dict[str, float]]:
    """
    An impossible layout where Row 1 and Row 2 have conflicting
    edge clearance requirements that prevent a global rafter alignment.
    """
    return [
        {"x": 0.0, "y": 0.0},
        {"x": 11.2, "y": 100.0} 
    ]


@pytest.fixture
def asymmetric_grid_data(default_settings: Settings) -> list[Panel]:
    """
    Asymmetric multi-row layout
    R1 - two panels with a gap at x=44.7
    R2 - one panel on the left ends at x=44.7
    R3 - one panel spanning across the center x=44.7, no joint boundar
    """
    w = default_settings.panel.width
    h = default_settings.panel.height
    return [
        Panel(Point(0.0, 0.0), w, h),
        Panel(Point(45.0, 0.0), w, h),
        
        Panel(Point(0.0, 71.6), w, h),
                
        Panel(Point(20.0, 143.2), w, h)
    ]