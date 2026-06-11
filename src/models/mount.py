from dataclasses import dataclass
from src.models.point import Point


@dataclass(frozen=True)
class Mount:
    """Represents a structural support attaching a solar array to the roof rafters."""
    position: Point

    def to_dict(self, precision: int | None = 3) -> dict[str, float]:
        return self.position.to_dict(precision=precision)