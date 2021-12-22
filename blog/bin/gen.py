#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.
from multiprocessing import Pool
from pathlib import Path
from subprocess import check_call
import os


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
        d = {}
        prev_file = None
        for file in files:
            d[file] = prev_file
            prev_file = file
        return d

    def format_blog(self, in_file: Path):
        os.chdir(in_file.parent)
        out_file = 'out/' + self._html_suffix(in_file)
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
        return in_file.name.removesuffix('.md') + '.html'


if __name__ == '__main__':
    generate_blog_posts()
