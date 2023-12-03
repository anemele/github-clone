""" GitHub clone.
    `git clone` from github.com into a folder named `{user}/{repo}`
    to avoid name collision.
"""
import argparse
import subprocess
from pathlib import Path
from typing import Iterable, Optional

from .config import CONFIG
from .constants import GIT_CONFIG_FILE, GITHUB_ROOT_PATH, SSH_URL
from .log import logger
from .parser import check, parse_url_batch


def git_clone(
    user: str,
    repo: str,
    dst: Optional[Path],
    *,
    config,
):
    url = f'{SSH_URL}{user}/{repo}.git'
    dst = GITHUB_ROOT_PATH / f'{user}/{dst or repo}'
    cmd = f'git clone {url} {dst} {config}'
    logger.info(cmd)
    cp = subprocess.run(cmd)
    if cp.returncode == 0:
        logger.info(f'done: {dst}, url={url}')
    else:
        logger.error(f'failed: {user}/{repo}')
        try:
            dst.parent.rmdir()
        except:
            pass


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(__package__, description=__doc__)
    parser.add_argument('url', type=str, nargs='*', help='github repo url')
    parser.add_argument(
        '-f',
        '--file',
        type=Path,
        help='read github repo url from a file, one line per url',
    )
    parser.add_argument(
        '-d',
        '--dest',
        type=Path,
        help='replace `user/repo` with `user/dest`',
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='do not clone, check validation',
    )
    parser.add_argument(
        '--config',
        help=f'git configs (wrapped with a pair of QUOTE). or save in a file: `{GIT_CONFIG_FILE}`',
        default='',
    )
    return parser


def get_url_list_from_file(file: Path) -> Iterable[str]:
    try:
        return (line.rstrip() for line in file.read_text().strip().splitlines())
    except Exception as e:
        logger.warning(e)

    return ()


def main():
    parser = create_parser()
    args = parser.parse_args()
    # print(args)
    # return

    args_file: Optional[Path] = args.file
    args_url: list[str] = args.url
    args_dest: Optional[Path] = args.dest
    args_check: bool = args.check
    args_config: str = args.config

    url_list = args_url
    if args_file is not None and args_file.is_file():
        url_list.extend(get_url_list_from_file(args_file))

    if len(url_list) == 0:
        parser.print_usage()
        return

    if args_check:
        check(url_list)
        return

    ur_list = parse_url_batch(url_list)
    config = f'{CONFIG} {args_config}'

    for user, repo in ur_list:
        git_clone(user, repo, args_dest, config=config)
