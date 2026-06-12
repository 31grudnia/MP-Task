import pytest
from dataclasses import replace
from config.settings import Settings
from src.services.rafter_optimizer import RafterOptimizer
from src.utils.layout_parser import LayoutParser
from src.utils.exceptions import InfeasibleLayoutError


def test_optimizer_finds_valid_offset_for_standard_layout(example_data: list[dict[str, float]], default_settings: Settings):
    """
    Tests that the optimizer successfully finds a valid rafter offset
    for the standard example layout, returning a float within [0.0, spacing).
    """
    parser = LayoutParser(settings=default_settings)
    segments = parser.parse(example_data)

    optimizer = RafterOptimizer(settings=default_settings)
    optimal_offset = optimizer.find_optimal_offset(segments)

    assert isinstance(optimal_offset, float)
    assert 0.0 <= optimal_offset < default_settings.rafter.spacing


def test_optimizer_raises_infeasible_layout_error_on_impossible_constraints(example_data: list[dict[str, float]], default_settings: Settings):
    """
    Tests that if constraints are mathematically impossible, 
    RafterOptimizer raises InfeasibleLayoutError instead of returning an offset.
    """
    impossible_mount_config = replace(
        default_settings.mount,
        edge_clearance=5.0,
        cantilever_limit=3.0
    )
    impossible_settings = replace(default_settings, mount=impossible_mount_config)

    parser = LayoutParser(settings=impossible_settings)
    segments = parser.parse(example_data)

    optimizer = RafterOptimizer(settings=impossible_settings)

    with pytest.raises(InfeasibleLayoutError, match="The solar panel layout is structurally infeasible"):
        optimizer.find_optimal_offset(segments)