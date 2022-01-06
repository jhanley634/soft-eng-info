#! /usr/bin/env python

# Copyright 2021 John Hanley. MIT licensed.
from multiprocessing import Pool
from pathlib import Path
from subprocess import check_output
import os

from bs4 import BeautifulSoup


def generate_blog_posts():
    bf = BlogFormatter()
    bf.toc()
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

    def toc(self):
        """Table of contents"""
        blog_dir = self.files[0].parent
        html = ('<!DOCTYPE html>\n<html lang="en"><head><title>soft-eng.info TOC</head>'
                '<body><h1>soft-eng.info</h1><ul>')
        for file in self.files:
            html += f'<li>{self._href(self._html_suffix(file), file.name)}</li>'
        with open(blog_dir / 'out/index.html', 'w') as fout:
            soup = BeautifulSoup(html, 'html.parser')
            fout.write(soup.prettify() + '\n')

    @staticmethod
    def _href(url, name):
        return f'<a href="{url}">{name}</a>'

    def format_blog(self, in_file: Path):
        os.chdir(in_file.parent)
        out_file = 'out/' + self._html_suffix(in_file)
        title = in_file.name.removesuffix('.md')
        # css = f'<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/3.18.1/build/cssreset/cssreset-min.css" />'
        # css += f' <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/3.18.1/build/cssbase/cssbase-min.css" />'
        css = f' <link rel="stylesheet" type="text/css" href="asset/pandoc.css" media="screen" />'
        cmd = (f'''(echo '<html lang="en"><head><title>{title}</title>{css}</head><body>';'''
               f' cat {in_file.name}; echo "{self._get_links(in_file)}"; cat common/footer.md)'
               f' | pandoc -w html')
        html = '<!DOCTYPE html>\n' + check_output(cmd, shell=True).decode()
        with open(out_file, 'w') as fout:
            soup = BeautifulSoup(html, 'html.parser')
            fout.write(soup.prettify() + '\n')

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
