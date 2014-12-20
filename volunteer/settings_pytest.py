import os
import dotenv

# This file exists just so that we can load the env variables during tests runs
# in a sane way but to keep them out of the main settings file.
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
dotenv.load_dotenv(os.path.join(PROJECT_PATH, ".env_defaults"))

from volunteer.settings import *  # NOQA
