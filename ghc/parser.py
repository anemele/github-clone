from typing import Iterable

from .consts import HTTP_URL, PATTERN
from .log import logger


def parse_url(url: str) -> tuple[str, str] | None:
    """parse github repo url,
    return (username, reponame)"""
    it = PATTERN.search(url)
    if it is None:
        return
    return it.group(1), it.group(2)


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
