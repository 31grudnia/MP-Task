from typing import Any

from config.settings import Settings
from src.models import Panel, Point, Segment
from src.utils.geometry import is_close
from src.utils.validator import validate_raw_input


class LayoutParser:
    """
    Parses, validates, and organizes raw coordinate layouts into domain models
    """
    def __init__(self, settings: Settings):
        self.settings = settings

    def parse(self, raw_data: list[dict[str, Any]]) -> list[Segment]:
        """
        Validates raw dictionary inputs, converts them to Panel instances
        and aggregates them into Segments.
        """
        
        validate_raw_input(raw_data)

        panels = [
            Panel(
                top_left=Point(x=float(item["x"]), y=float(item["y"])),
                width=self.settings.panel.width,
                height=self.settings.panel.height
            )
            for item in raw_data
        ]

        return self._group_into_segments(panels)

    def _group_into_segments(self, panels: list[Panel]) -> list[Segment]:
        """
        Helper to align panels into rows and segment them based 
        on horizontal proximity.
        """
        if not panels:
            return []

        rows: dict[float, list[Panel]] = {}
        for panel in panels:
            row_key = None
            for existing_y in rows:
                if is_close(panel.top, existing_y):
                    row_key = existing_y
                    break
            
            if row_key is None:
                row_key = panel.top
                rows[row_key] = []
            
            rows[row_key].append(panel)

        segments: list[Segment] = []

        for y_coord in sorted(rows.keys()):
            
            row_panels = sorted(rows[y_coord], key=lambda p: p.left)
            current_segment_panels = [row_panels[0]]
            
            for next_panel in row_panels[1:]:
                previous_panel = current_segment_panels[-1]
                gap = next_panel.left - previous_panel.right
                
                if gap < self.settings.joint.horizontal_gap_threshold:
                    current_segment_panels.append(next_panel)
                else:
                    segments.append(Segment(current_segment_panels))
                    current_segment_panels = [next_panel]
            
            segments.append(Segment(current_segment_panels))

        return segments