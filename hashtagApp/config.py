"""Application configuration."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
IMAGE_SIZE = int(os.getenv("IMAGE_SIZE", "400"))
