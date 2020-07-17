# python imports
import os

# third-party imports
from dotenv import load_dotenv

load_dotenv(verbose=True)
env_path = os.path.join(os.path.abspath(os.path.join('.env', os.pardir)), '.env')
load_dotenv(dotenv_path=env_path)
