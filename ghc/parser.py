import re
from typing import Iterable

from .consts import HTTP_URL
from .log import logger

PATTERN = re.compile(r'^(?:https://[\w\.\-]+/)|(?:git@[\w\.\-]+:)')


def parse_url(url: str) -> tuple[str, str] | None:
    """parse github repo url,
    return (username, reponame)"""
    s = PATTERN.search(url)
    if s is not None:
        url = url[s.end() :]

    it = url.removeprefix('/').split('/', 2)
    match len(it):
        case 1:
            return
        case 2:
            return it[0], it[1].removesuffix('.git')
        case 3:
            return it[0], it[1]


def parse_url_batch(url_list: Iterable[str]) -> Iterable[tuple[str, str]]:
    for url in url_list:
        sth = parse_url(url)
        if sth is None:
            logger.warning(f'invalid url: {url}')
            continue
        yield sth


def check(url_list: list[str]) -> None:
    ur_list = parse_url_batch(url_list)
    for u, r in ur_list:
        url = f'{HTTP_URL}{u}/{r}.git'
        logger.info(f'{url}')
