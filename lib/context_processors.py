import tomllib
from datetime import datetime, timezone
from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=1)
def get_version():
    """Get version from pyproject.toml, cached for performance."""
    try:
        pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        return data.get("project", {}).get("version", "unknown")
    except Exception:
        return "unknown"


def inject_global_context(request):
    return {
        "utcnow": datetime.now(timezone.utc),
        "version": get_version(),
    }
