from dataclasses import dataclass

from src.models.point import Point


@dataclass(frozen=True)
class Panel:
    """
    Represents an individual solar panel defined by its top-left corner and physical dimensions.
    """
    top_left: Point
    width: float
    height: float

    @property
    def left(self) -> float:
        """The absolute horizontal X coordinate of the left edge."""
        return self.top_left.x

    @property
    def right(self) -> float:
        """The absolute horizontal X coordinate of the right edge."""
        return self.top_left.x + self.width

    @property
    def top(self) -> float:
        """The absolute vertical Y coordinate of the top edge."""
        return self.top_left.y

    @property
    def bottom(self) -> float:
        """The absolute vertical Y coordinate of the bottom edge."""
        return self.top_left.y + self.height

    def to_dict(self, precision: int | None = None) -> dict[str, float]:
        return {
            "x": round(self.left, precision) if precision is not None else self.left,
            "y": round(self.top, precision) if precision is not None else self.top,
            "width": self.width,
            "height": self.height
        }