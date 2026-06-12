from dataclasses import replace

from config.settings import Settings
from src.models import Point, Panel, Segment
from src.services.mount_calculator import MountCalculator


def test_single_panel_forces_at_least_two_mounts(default_settings: Settings):
    """
    single panel must receive at least 2 mounts
    to satisfy the cantilever limit on both sides.
    """
    panel = Panel(
        top_left=Point(0.0, 0.0),
        width=default_settings.panel.width,
        height=default_settings.panel.height
    )
    segment = Segment(panels=[panel])
    
    test_rafter = replace(default_settings.rafter, first_rafter_x=8.0)
    test_settings = replace(default_settings, rafter=test_rafter)
    
    calculator = MountCalculator(settings=test_settings)
    mounts = calculator.calculate_mounts(segments=[segment])
    
    top_rail_x = [m.position.x for m in mounts if m.position.y == 0.0]
    
    assert len(top_rail_x) >= 2, "A single panel must have at least 2 mounts per rail."


def test_mounts_respect_edge_clearance(default_settings: Settings):
    """
    Asserts that no mount is closer than the edge clearance 2.0
    to any panels horizontal boundaries.
    """
    panel = Panel(Point(0.0, 0.0), default_settings.panel.width, default_settings.panel.height)
    segment = Segment(panels=[panel])
    
    test_rafter = replace(default_settings.rafter, first_rafter_x=8.0)
    test_settings = replace(default_settings, rafter=test_rafter)
    
    calculator = MountCalculator(settings=test_settings)
    mounts = calculator.calculate_mounts(segments=[segment])
    
    clearance = default_settings.mount.edge_clearance
    panel_right = panel.right
    
    for m in mounts:
        assert m.position.x >= panel.left + clearance, f"Mount at {m.position.x} violates left edge clearance."
        assert m.position.x <= panel_right - clearance, f"Mount at {m.position.x} violates right edge clearance."


def test_mounts_satisfy_span_limit(default_settings: Settings):
    """
    Asserts that the distance between any two consecutive mounts on the same 
    rail does not exceed the span limit 48.0 units
    """
    w = default_settings.panel.width
    h = default_settings.panel.height
    panels = [
        Panel(Point(0.0, 0.0), w, h),
        Panel(Point(45.0, 0.0), w, h),
        Panel(Point(90.0, 0.0), w, h)
    ]
    segment = Segment(panels=panels)
    
    test_rafter = replace(default_settings.rafter, first_rafter_x=8.0)
    test_settings = replace(default_settings, rafter=test_rafter)
    
    calculator = MountCalculator(settings=test_settings)
    mounts = calculator.calculate_mounts(segments=[segment])
    
    top_mounts_x = sorted([m.position.x for m in mounts if m.position.y == 0.0])
    
    for i in range(len(top_mounts_x) - 1):
        span = top_mounts_x[i+1] - top_mounts_x[i]
        assert span <= default_settings.mount.span_limit, \
            f"Span of {span} exceeds max of {default_settings.mount.span_limit}"