from dataclasses import replace

from config.settings import Settings
from src.models import Segment
from src.services.mount_calculator import MountCalculator
from src.utils.exceptions import InfeasibleLayoutError


class RafterOptimizer:
    """
    Optimization service responsible for finding the most cost-effective rafter alignment.
    """
    def __init__(self, settings: Settings):
        self.settings = settings

    def find_optimal_offset(self, segments: list[Segment], step: float = 0.5) -> float:
        """
        Performs a grid search over one rafter spacing period [0.0, spacing)
        to find the offset that requires the minimum number of support mounts.
        """
        spacing = self.settings.rafter.spacing
        best_offset = None
        min_mounts_count = float("inf")

        # determine the search steps based on the rafter spacing and grid step size
        num_steps = int(spacing / step)

        for i in range(num_steps):
            test_offset = i * step

            test_rafter_config = replace(self.settings.rafter, first_rafter_x=test_offset)
            test_settings = replace(self.settings, rafter=test_rafter_config)

            calculator = MountCalculator(test_settings)

            try:
                mounts = calculator.calculate_mounts(segments)
                mounts_count = len(mounts)

                if mounts_count < min_mounts_count:
                    min_mounts_count = mounts_count
                    best_offset = test_offset

            except InfeasibleLayoutError:
                # Iignore configurations that violate cantilever or span limits
                continue

        # if no offset yields a valid support structure, the entire array is unsupported
        if best_offset is None:
            raise InfeasibleLayoutError(
                "The solar panel layout is structurally infeasible. "
                "No rafter offset can satisfy the required Cantilever and Span limits."
            )

        return best_offset