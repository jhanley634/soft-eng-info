#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.
from multiprocessing import Pool
from pathlib import Path
from subprocess import check_call
import os
import re


def generate_blog_posts():
    bf = BlogFormatter()
    with Pool() as p:
        p.map(bf.format_blog, bf.files)


class BlogFormatter:

    def __init__(self, folder=Path(__file__ + '../../..').resolve()):
        self.files = sorted(folder.glob('*.md'))

        self.prev = self._fill_in(self.files)

        self.next = self._fill_in(reversed(self.files))

    @staticmethod
    def _fill_in(files: list) -> dict:
        prev = {}
        prev_file = None
        for file in files:
            prev[file] = prev_file
            prev_file = file
        return prev

    def format_blog(self, in_file: Path):
        os.chdir(in_file.parent)
        markdown_suffix_re = re.compile(r'\.md$')
        assert markdown_suffix_re.search(f'{in_file}')
        out_file = 'out/' + markdown_suffix_re.sub('.html', in_file.name)
        cmd = f'(cat {in_file.name}; echo "{self._get_links(in_file)}"; cat common/footer.md) | pandoc -o {out_file}'
        check_call(cmd, shell=True)

    def _get_links(self, in_file: Path):
        links = '\n\n'
        if self.prev[in_file]:
            links += f'[prev]({self._html_suffix(self.prev[in_file])})\n'
        if self.next[in_file]:
            links += f'[next]({self._html_suffix(self.next[in_file])})\n'
        return links

    @staticmethod
    def _html_suffix(in_file: Path) -> str:
        md_re = re.compile(r'\.md$')
        return md_re.sub('.html', f'{in_file.name}')


if __name__ == '__main__':
    generate_blog_posts()
