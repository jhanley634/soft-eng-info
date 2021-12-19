#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.

from multiprocessing import Pool
from pathlib import Path
from subprocess import check_call
import os
import re


def generate_blog_posts(folder=Path(__file__ + '../../..').resolve()):
    with Pool() as p:
        p.map(format_blog, sorted(folder.glob('*.md')))


def format_blog(in_file: Path):
    os.chdir(in_file.parent)
    markdown_suffix_re = re.compile(r'\.md$')
    assert markdown_suffix_re.search(f'{in_file}')
    out_file = 'out/' + markdown_suffix_re.sub('.html', in_file.name)
    cmd = f'(cat {in_file.name} common/footer.md) | pandoc -o {out_file}'
    check_call(cmd, shell=True)


if __name__ == '__main__':
    generate_blog_posts()
