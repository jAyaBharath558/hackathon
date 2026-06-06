import logging
import sys
from pathlib import Path


def get_logger(name: str = "RAGChatbot") -> logging.Logger:
    """
    Initialize and return a logger instance
    """
    logger = logging.getLogger(name)
    
    # Set log level
    logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger
