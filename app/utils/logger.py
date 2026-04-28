import logging
import sys

def setup_logging():
    log_level = logging.DEBUG if __import__("app.config", fromlist=["settings"]).settings.DEBUG else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Set uvicorn access log to same level
    logging.getLogger("uvicorn.access").setLevel(log_level)