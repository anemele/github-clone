import os.path
import tomllib

from .constants import GIT_CONFIG_FILE, GITHUB_ROOT_PATH

with open(os.path.join(GITHUB_ROOT_PATH, GIT_CONFIG_FILE), 'rb') as fp:
    config = tomllib.load(fp)

config = config.get('config')
assert config is not None

CONFIG = ' '.join(f'--{k}={v}' for k, v in config.items())
