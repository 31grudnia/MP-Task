from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def to_dict(self, precision: int | None = None) -> dict[str, float]:
        if precision is not None:
            return {
                "x": round(self.x, precision),
                "y": round(self.y, precision)
            }
        return {
            "x": self.x,
            "y": self.y
        }

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"