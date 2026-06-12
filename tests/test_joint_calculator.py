from config.settings import Settings
from src.models import Panel, Segment, Point
from src.services.joint_calculator import JointCalculator
from src.utils.layout_parser import LayoutParser



def test_asymmetric_grid_does_not_generate_false_joints(asymmetric_grid_data: list[Panel], default_settings: Settings):
    """
    Ensure that vertical boundaries do not group solid 
    spanning panels below them if they do not contain a joint boundary themselves.
    """
    row1 = Segment(panels=[asymmetric_grid_data[0], asymmetric_grid_data[1]])
    row2 = Segment(panels=[asymmetric_grid_data[2]])
    row3 = Segment(panels=[asymmetric_grid_data[3]])
    
    calculator = JointCalculator(settings=default_settings)
    joints = calculator.calculate_joints(segments=[row1, row2, row3])
    
    # A joint should exist at the midpoint between Row 1 and Row 2 y=71.35
    # But NO joint should exist at the midpoint between Row 2 and Row 3 y=142.95 near x=44.7
    # because Row 3 is a solid piece spanning across it.
    joints_near_row3_boundary = [
        j for j in joints 
        if abs(j.position.x - 44.85) < 1.0 and abs(j.position.y - 142.95) < 1.0
    ]
    
    assert len(joints_near_row3_boundary) == 0, \
        "False joint generated over a solid, non-divided panel in Row 3."


def test_float_precision_on_borderline_gaps(default_settings: Settings):
    """
    floating-point tolerances on boundary gaps.
    gap of 0.9999 should trigger a joint while a gap of 1.0001 should not.
    """
    w = default_settings.panel.width
    parser = LayoutParser(settings=default_settings)
    
    raw_close = [
        {"x": 0.0, "y": 0.0},
        {"x": w + 0.999, "y": 0.0}
    ]
    segments_close = parser.parse(raw_close)
    
    raw_far = [
        {"x": 0.0, "y": 0.0},
        {"x": w + 1.001, "y": 0.0}
    ]
    segments_far = parser.parse(raw_far)
    
    calculator = JointCalculator(settings=default_settings)
    
    joints_close = calculator.calculate_joints(segments=segments_close)
    joints_far = calculator.calculate_joints(segments=segments_far)
    
    assert len(joints_close) > 0, "Joint was not triggered for gap < 1.0 threshold"
    assert len(joints_far) == 0, "Joint was incorrectly triggered for gap > 1.0 threshold"