from pathlib import Path

def get_data_dir() -> Path:
    """Return a consistent data directory for the project, creating it if needed."""
    data_dir = Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir