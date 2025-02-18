import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

def load_json(file_path, default=None):
    """Load JSON data from a file."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            logger.debug(f"Loaded data from {file_path}: {data}")
            return data
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        logger.debug(f"Error loading {file_path}: {e}. Returning default: {default}")
        return default

def save_json(file_path, data):
    """Save JSON data to a file."""
    logger.debug(f"Saving data to {file_path}: {data}")
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except PermissionError as e:
        logger.error(f"Error saving to {file_path}: {e}")