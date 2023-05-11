import logging
import sys

# Configure logging to write to a file
file_handler = logging.FileHandler(filename='app.log', mode='a')
file_handler.setLevel(logging.ERROR)

# Configure logging to write to the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Configure the logging format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
