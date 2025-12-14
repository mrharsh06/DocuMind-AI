import logging
import os
from logging.handlers import RotatingFileHandler
from app.config import settings

def setup_logging():
    """
    Configure logging for the entire application.
    Sets up both console and file logging with rotation.
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    root_logger=logging.getLogger()
    root_logger.setLevel(log_level)

    root_logger.handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "documind.log"),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5  # Keep 5 backup files
    )

    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    
    return root_logger
    



