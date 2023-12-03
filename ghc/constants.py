import re
from pathlib import Path

GITHUB_ROOT_PATH = Path('D:\\work\\github')
GIT_CONFIG_FILE = 'config.toml'

HTTP_URL = 'https://github.com/'
SSH_URL = 'git@github.com:'
GITHUB_URL_LIST = (
    HTTP_URL,
    SSH_URL,
    'https://hub.nuaa.cf/',
    'https://hub.yzuu.cf/',
)
PATTERN = re.compile(r'[/:]?([\w-]+)/([\w.-]+?)(?:\.git)?$')
