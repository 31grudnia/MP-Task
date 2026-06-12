from config.settings import Settings
from src.models import Segment, Joint, Point
from src.services.interfaces import JointCalculatorInterface


class JointCalculator(JointCalculatorInterface):
    """
    Stateless calculator for inter-panel connection joints.
    """
    def __init__(self, settings: Settings):
        self.settings = settings

    def calculate_joints(self, segments: list[Segment]) -> list[Joint]:
        """
        Calculates unique center coordinates of joints connecting adjacent panels.
        """
        y_tops = sorted(list({segment.y for segment in segments}))
        y_bottoms = sorted(list({segment.y + self.settings.panel.height for segment in segments}))

        y_mapping: dict[float, float] = {}
        for y in y_tops + y_bottoms:
            y_mapping[y] = y

        for y_bottom in y_bottoms:
            for y_top in y_tops:
                gap = y_top - y_bottom
                if 0 <= gap < self.settings.joint.vertical_gap_threshold:
                    shared_y = (y_bottom + y_top) / 2.0
                    y_mapping[y_bottom] = shared_y
                    y_mapping[y_top] = shared_y

        unique_joints: dict[tuple[float, float], Joint] = {}

        for segment in segments:
            # segment with N panels has N-1 horizontal boundaries
            for i in range(len(segment.panels) - 1):
                panel_left = segment.panels[i]
                panel_right = segment.panels[i + 1]

                joint_x = (panel_left.right + panel_right.left) / 2.0

                for raw_y in [segment.y, segment.y + self.settings.panel.height]:
                    final_y = y_mapping[raw_y]

                    coord_key = (round(joint_x, 5), round(final_y, 5))
                    if coord_key not in unique_joints:
                        unique_joints[coord_key] = Joint(position=Point(joint_x, final_y))

        return list(unique_joints.values())