from dataclasses import dataclass
from src.models.point import Point


@dataclass(frozen=True)
class Joint:
    """Represents a connector used to secure adjacent solar panels together."""
    position: Point

    def to_dict(self, precision: int | None = 3) -> dict[str, float]:
        return self.position.to_dict(precision=precision)