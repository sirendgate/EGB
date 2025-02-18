import logging

def setup_logging(level=logging.INFO):
    """
    Sets up the logging configuration.
    
    Args:
        level (int): The logging level. Default is logging.INFO.
    """
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=level
    )