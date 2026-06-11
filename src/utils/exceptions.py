class InfeasibleLayoutError(Exception):
    """Raised when the given solar panel layout violates physical or structural constraints."""
    pass


class ValidationError(Exception):
    """Raised when raw input coordinates format, structure, or values are invalid."""
    pass