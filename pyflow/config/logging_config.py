import logging
from pathlib import Path

def setup_logging() -> None:
    log_dir = Path("pyflow/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "app.log"
    logging.basicConfig(
        level = logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
        force=True
    )