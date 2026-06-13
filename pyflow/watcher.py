import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from extractors import get_extractor
from utils import load_config
from config.logging_config import setup_logging
from main import process_file

setup_logging()
logger = logging.getLogger(__name__)
config = load_config()

class FileArrivalHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = event.src_path

        logger.info(f"New file detected: {file_path}")

        try:
            time.sleep(2)
            process_file(file_path)
        
        except Exception as e:
            logger.exception(f"Failed processing {file_path}: {e}")

def watch_directory() -> None:
    
    watch_path = config['etl']['input_path']

    observer = Observer()

    observer.schedule(
        FileArrivalHandler(),
        path=watch_path,
        recursive=False
    )

    observer.start()

    logger.info(f"Watching directory: {watch_path}")

    try:
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("Stopping file watcher...")
        observer.stop()

    observer.join()

if __name__ == '__main__':
    watch_directory()