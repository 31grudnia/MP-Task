from abc import ABC, abstractmethod

from src.models import Segment, Mount, Joint


class MountCalculatorInterface(ABC):
    """Interface for structural support (mount) calculation strategies."""

    @abstractmethod
    def calculate_mounts(self, segments: list[Segment]) -> list[Mount]:
        """Calculates support coordinates for the given segments."""
        pass


class JointCalculatorInterface(ABC):
    """Interface for inter-panel connection (joint) calculation strategies."""

    @abstractmethod
    def calculate_joints(self, segments: list[Segment]) -> list[Joint]:
        """Calculates joint coordinates for the given segments."""
        pass