#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''fetches undownloaded posts from atcoder.jp'''

import os
import re
import sys
import time
import urllib2

def main():
    try:
        from saved_posts import SAVED_POSTS
    except ImportError:
        SAVED_POSTS = set()

    if not os.path.isdir('posts/'):
        os.mkdir('posts/')

    index_re = re.compile(r'<a href="/post/(\d+)">')
    suffix = time.strftime('%Y%m%d%H%M%S')
    i = 1
    while True:
        inname = 'https://atcoder.jp/?lang=ja&p={}'.format(i)
        outname = 'posts/index_{}_{}.html'.format(suffix, i)

        contents = urllib2.urlopen(inname).read()
        posts = set(map(int, index_re.findall(contents)))
        if posts.issubset(SAVED_POSTS):
            break

        SAVED_POSTS |= posts
        with open(outname, 'w') as fout:
            fout.write(contents)
            print 'Saved:', outname

        if not posts.isdisjoint(SAVED_POSTS):
            break

        i += 1

    with open('saved_posts.py', 'w') as fout:
        fout.write("# This file is generated by 'fetch_posts.py'\n")
        fout.write('SAVED_POSTS = {}\n'.format(SAVED_POSTS))

if __name__ == '__main__':
    main()
