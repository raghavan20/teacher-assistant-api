import logging


class Registry:
    s_db = None
    app = None


def get_logger(name="teacher-assistant-api"):
    """Initializes and returns a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs

    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Set formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    if not logger.handlers:  # Prevent duplicate handlers
        logger.addHandler(handler)

    return logger