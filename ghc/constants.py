import re

GITHUB_ROOT_PATH = 'D:\\work\\github'
GIT_CONFIG_FILE = 'config.toml'

GITHUB_HTTP = 'https://github.com/'
GITHUB_URL_LIST = (
    GITHUB_HTTP,
    'git@github.com:',
    'https://hub.nuaa.cf/',
    'https://hub.yzuu.cf/',
)
PATTERN = re.compile(r'[/:]?([\w-]+)/([\w.-]+?)(?:\.git)?$')
