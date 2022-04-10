from pathlib import PurePath
import os

# root of the whole project
PROJECT_ROOT=os.path.abspath(PurePath(__file__).parents[1])
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')