""" GitHub clone.
git clone from github.com or its mirror sites
into a folder named {user}/{repo}
to avoid name collision.
"""
import argparse
import os
import os.path
import subprocess
from typing import Optional

from .config import CONFIG
from .constants import GITHUB_ROOT_PATH, GITHUB_URL_LIST
from .parser import check, parse_url_batch
from .types import Ls_Gs


def git_clone(ur: str, dst: str, *, config) -> str:
    dst = os.path.join(GITHUB_ROOT_PATH, dst)
    if os.path.exists(dst) and os.listdir(dst):
        return f'[ERROR] exists: {dst}'

    for github in GITHUB_URL_LIST:
        url = f'{github}{ur}.git'
        # return True
        # NOTICE! Here clones into a folder named `user/repo`
        cmd = f'git clone {url} {dst} {config}'
        print(cmd)
        cp = subprocess.run(cmd)
        if cp.returncode == 0:
            return f'[INFO] done: {ur}, url: {url}'

    return f'[ERROR] failed: {ur}'


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(__package__, description=__doc__)
    parser.add_argument('url', type=str, nargs='*', help='github repo url')
    parser.add_argument(
        '-f',
        '--file',
        type=str,
        help='read github repo url from a file, one line per url',
    )
    parser.add_argument(
        '-n',
        '--no-user',
        action='store_true',
        help='use `repo` instead of `user/repo`',
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='do not clone, check validation',
    )
    parser.add_argument(
        '--config',
        help='temp config',
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    # print(args)
    # return

    args_file: str = args.file
    args_url: list[str] = args.url
    args_check: bool = args.check
    args_no_user: bool = args.no_user
    args_config: Optional[str] = args.config

    url_list: Ls_Gs
    if args_file is not None and os.path.isfile(args_file):
        try:
            with open(args_file) as fp:
                url_list = (line.rstrip() for line in fp.readlines())
        except Exception as e:
            print(e)
            url_list = args_url
    else:
        if len(args_url) == 0:
            parser.print_usage()
            return

        url_list = args_url

    if args_check:
        check(url_list)
        return

    ur_list = parse_url_batch(url_list)
    if args_config is not None:
        config = f'{CONFIG} {args_config}'
    else:
        config = CONFIG
    for user, repo in ur_list:
        ur = f'{user}/{repo}'
        dst = repo if args_no_user else ur
        msg = git_clone(ur, dst, config=config)
        print(msg)
