import json
import sys

from src.services.solar_array_service import SolarArrayService
from src.utils.exceptions import InfeasibleLayoutError, ValidationError

EXAMPLE_DATA = [
    {"x": 0, "y": 0}, {"x": 45.05, "y": 0}, {"x": 90.1, "y": 0},
    {"x": 0, "y": 71.6}, {"x": 135.15, "y": 0}, {"x": 135.15, "y": 71.6},
    {"x": 0, "y": 143.2}, {"x": 45.05, "y": 143.2}, {"x": 135.15, "y": 143.2},
    {"x": 90.1, "y": 143.2}
]


def main() -> None:
    print("=" * 60)
    print("          SOLAR ARRAY CALCULATOR - PIPELINE RUN          ")
    print("=" * 60)
    
    service = SolarArrayService()
    
    try:
        print("[INFO] Processing layout with Rafter Optimization enabled...")
        
        output = service.process_layout(EXAMPLE_DATA, precision=3, optimize_rafters=True)
        
        print("\n[SUCCESS] Calculation finished successfully!")
        print("-" * 60)
        print(f"Total Structural Supports (Mounts): {len(output['mounts'])}")
        print(f"Total Inter-panel Joints:          {len(output['joints'])}")
        print("-" * 60)
        
        print("\n[OUTPUT] Serialized JSON Result:")
        print(json.dumps(output, indent=2))
        
    except ValidationError as e:
        print(f"\n[ERROR] Input validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except InfeasibleLayoutError as e:
        print(f"\n[ERROR] Structurally infeasible layout: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[CRITICAL] Unexpected execution error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()