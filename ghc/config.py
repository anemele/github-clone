import tomllib

from .constants import GIT_CONFIG_FILE, GITHUB_ROOT_PATH


def _get_config() -> str:
    file = GITHUB_ROOT_PATH / GIT_CONFIG_FILE
    if not file.exists():
        return ''

    with open(file, 'rb') as fp:
        config = tomllib.load(fp)

    return ' '.join(f'--{k}={v}' for k, v in config.get('config', {}).items())


CONFIG = _get_config()
