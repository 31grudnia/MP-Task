from config.settings import Settings
from src.utils.layout_parser import LayoutParser


def test_broken_tooth_layout_segments_correctly(default_settings: Settings):
    """
    single row with a gap of 55.3 units
    must be correctly partitioned into 2 distinct Segment objects.
    """
    raw_data = [
        {"x": 0.0, "y": 0.0},
        {"x": 100.0, "y": 0.0}
    ]
    parser = LayoutParser(settings=default_settings)
    segments = parser.parse(raw_data)
    
    assert len(segments) == 2, f"Expected 2 segments for the 'Broken Tooth' layout, got {len(segments)}."
    assert segments[0].x_start == 0.0
    assert segments[1].x_start == 100.0