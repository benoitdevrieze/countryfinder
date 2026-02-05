import os

DEFAULT_DATA_DIR = os.getenv('DATA_PATH') or os.path.join(os.path.dirname(__file__), 'data')
