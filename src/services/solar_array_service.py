from typing import Any
from dataclasses import replace

from config.settings import Settings, DEFAULT_SETTINGS
from src.services.interfaces import MountCalculatorInterface, JointCalculatorInterface
from src.services.mount_calculator import MountCalculator
from src.services.joint_calculator import JointCalculator
from src.services.rafter_optimizer import RafterOptimizer
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

    def process_layout(
        self,
        raw_data: list[dict[str, Any]],
        precision: int | None = 3,
        optimize_rafters: bool = False
    ) -> dict[str, list[dict[str, float]]]:
        """
        Coordinates parsing, support placement, and joint calculation.
        """
        segments = self.parser.parse(raw_data)

        active_settings = self.settings
        active_mount_calc = self.mount_calculator
        active_joint_calc = self.joint_calculator

        if optimize_rafters:
            optimizer = RafterOptimizer(self.settings)
            best_offset = optimizer.find_optimal_offset(segments)

            optimized_rafter = replace(self.settings.rafter, first_rafter_x=best_offset)
            active_settings = replace(self.settings, rafter=optimized_rafter)

            active_mount_calc = MountCalculator(active_settings)
            active_joint_calc = JointCalculator(active_settings)

        mount_entities = active_mount_calc.calculate_mounts(segments)

        joint_entities = active_joint_calc.calculate_joints(segments)

        return {
            "mounts": [mount.to_dict(precision=precision) for mount in mount_entities],
            "joints": [joint.to_dict(precision=precision) for joint in joint_entities],
        }