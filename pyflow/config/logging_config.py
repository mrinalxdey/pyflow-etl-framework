import logging

def setup_logging() -> None:
    logging.basicConfig(
        level = logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ],
        force=True
    )