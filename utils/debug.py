import logging

def setup_logging(log_file="debug.log"):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def log_debug(message):
    logging.debug(message)

def log_error(message):
    logging.error(message)

def log_info(message):
    logging.info(message)

# Example usage
if __name__ == "__main__":
    setup_logging()
    log_debug("This is a debug message")
    log_info("This is an info message")
    log_error("This is an error message")
