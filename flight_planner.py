"""
Top-level shim to re-export the implementation from `src/flight_planner.py`.

This allows tests to import `flight_planner` while keeping the real
implementation inside the `src/` directory.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

# Load the implementation file from `src/flight_planner.py` under a
# private module name to avoid recursive import of this shim.
_impl_path = Path(__file__).parent / "src" / "flight_planner.py"
spec = importlib.util.spec_from_file_location("_flight_planner_impl", str(_impl_path))
_impl = importlib.util.module_from_spec(spec)
# Register module before executing so dataclasses and typing can find it
if spec and spec.name:
    sys.modules[spec.name] = _impl
# Execute the module in its own namespace
spec.loader.exec_module(_impl)  # type: ignore

# Re-export public names from the implementation module into this module's
# globals so that `from flight_planner import X` works as expected in tests.
for _name in dir(_impl):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_impl, _name)

__all__ = [n for n in dir() if not n.startswith("_")]
