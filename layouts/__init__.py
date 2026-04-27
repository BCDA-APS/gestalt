from pathlib import Path

_package_dir = Path(__file__).parent

__all__ = [ f.name for f in _package_dir.iterdir() if f.is_dir() and f.name != "__pycache__" ]

__all__.append("registry")
