import logging

def setup_logger(name="port_scanner", level=logging.INFO):
    """Defines a function called setup_logger that accepts name and logging level"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Console handler
        stream_handler = logging.StreamHandler() #creates a handler  that sends messages to the console
        stream_formatter = logging.Formatter( #Defines the format of log messages for the console.
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        # File handler
        file_handler = logging.FileHandler("scanner.log")
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    logger.setLevel(level)
    return logger
