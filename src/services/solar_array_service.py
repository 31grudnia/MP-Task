
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

    def process_layout(self, raw_data: list[dict[str, Any]]) -> dict[str, list[dict[str, float]]]:
        """
        Coordinates parsing, support placement, and joint calculation.
        """
        # 1. Parse raw coordinates into domain segment structures
        segments = self.parser.parse(raw_data)

        # 2. Calculate support mounts
        mount_entities = self.mount_calculator.calculate_mounts(segments)

        # 3. Calculate inter-panel joints
        joint_entities = self.joint_calculator.calculate_joints(segments)

        # 4. Serialize outputs (precision rounding occurs only here at the export layer)
        return {
            "mounts": [mount.to_dict() for mount in mount_entities],
            "joints": [joint.to_dict() for joint in joint_entities],
        }