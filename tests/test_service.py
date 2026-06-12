import pytest

from dataclasses import replace

from config.settings import Settings
from src.services import SolarArrayService
from src.utils.exceptions import InfeasibleLayoutError


def test_impossible_roof_raises_infeasible_layout_error(impossible_roof_data: list[dict[str, float]], default_settings: Settings):
    """
    Verifies that if no global rafter offset is mathematically 
    capable of satisfying constraints, a clean custom exception is raised.
    """
    impossible_mount_config = replace(
        default_settings.mount,
        edge_clearance=5.0,
        cantilever_limit=3.0
    )
    impossible_settings = replace(default_settings, mount=impossible_mount_config)
    
    service = SolarArrayService(settings=impossible_settings)
    
    with pytest.raises(InfeasibleLayoutError, match="The solar panel layout is structurally infeasible"):
        service.process_layout(impossible_roof_data, optimize_rafters=True)


def test_example_reproduces_valid_structure(example_data: list[dict[str, float]], default_settings: Settings):
    """
    verify that the complete service runs successfully
    """
    service = SolarArrayService(settings=default_settings)
    output = service.process_layout(example_data, optimize_rafters=True)
    
    assert "mounts" in output
    assert "joints" in output
    assert len(output["mounts"]) > 0
    assert len(output["joints"]) > 0
    
    for mount in output["mounts"]:
        assert "x" in mount and "y" in mount
        assert isinstance(mount["x"], float)
        assert isinstance(mount["y"], float)