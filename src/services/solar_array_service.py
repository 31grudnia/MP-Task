
from typing import Any
from config.settings import Settings, DEFAULT_SETTINGS
from src.services.interfaces import MountCalculatorInterface, JointCalculatorInterface
from src.services.mount_calculator import MountCalculator
from src.services.joint_calculator import JointCalculator
from src.utils.layout_parser import LayoutParser


class SolarArrayService:
    """
    Orchestrator for processing raw solar array layouts.
    """
    def __init__(
        self,
        settings: Settings = DEFAULT_SETTINGS,
        mount_calculator: MountCalculatorInterface | None = None,
        joint_calculator: JointCalculatorInterface | None = None,
    ):
        self.settings = settings
        self.parser = LayoutParser(settings)
        self.mount_calculator = mount_calculator or MountCalculator(settings)
        self.joint_calculator = joint_calculator or JointCalculator(settings)


    def process_layout(self, 
                       raw_data: list[dict[str, Any]],
                       precision: int | None = 3
        ) -> dict[str, list[dict[str, float]]]:
        """
        Coordinates parsing, support placement, and joint calculation.
        """
        segments = self.parser.parse(raw_data)
        mount_entities = self.mount_calculator.calculate_mounts(segments)
        joint_entities = self.joint_calculator.calculate_joints(segments)

        return {
            "mounts": [mount.to_dict(precision=precision) for mount in mount_entities],
            "joints": [joint.to_dict(precision=precision) for joint in joint_entities],
        }