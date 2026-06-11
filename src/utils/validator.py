from typing import Any


class ValidationError(Exception):
    """Custom exception raised when raw input coordinates validation fails."""
    pass


def validate_raw_input(data: Any) -> None:
    """Validates the structure and consistency of the raw input coordinate list."""
    if not isinstance(data, list):
        raise ValidationError("Input data must be a list of panel coordinates.")

    seen_coordinates: set[tuple[float, float]] = set()

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValidationError(f"Item at index {index} is not a dictionary.")

        if "x" not in item or "y" not in item:
            raise ValidationError(f"Item at index {index} is missing 'x' or 'y' keys.")

        try:
            x = float(item["x"])
            y = float(item["y"])
        except (ValueError, TypeError):
            raise ValidationError(
                f"Coordinates at index {index} must be valid numerical values."
            )

        coord_key = (round(x, 5), round(y, 5))
        if coord_key in seen_coordinates:
            raise ValidationError(
                f"Duplicate panel coordinates detected at: x={x}, y={y}."
            )
            
        seen_coordinates.add(coord_key)