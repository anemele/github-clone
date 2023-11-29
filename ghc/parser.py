from typing import Optional

from .constants import GITHUB_HTTP, PATTERN
from .types import G_Ts, Ls_Gs


def parse_url(url: str) -> Optional[tuple[str, str]]:
    """parse github repo url,
    return (username, reponame)"""
    it = PATTERN.search(url)
    if it is None:
        return
    return it.group(1), it.group(2)


def parse_url_batch(url_list: Ls_Gs) -> G_Ts:
    for url in url_list:
        sth = parse_url(url)
        if sth is None:
            print(f'[ERROR] invalid url: {url}')
            continue
        yield sth


def check(url_list: Ls_Gs) -> None:
    ur_list = parse_url_batch(url_list)
    for u, r in ur_list:
        url = f'{GITHUB_HTTP}{u}/{r}.git'
        print(url)
