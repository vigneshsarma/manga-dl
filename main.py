#!/usr/bin/env python -u
import sys

from parser import mangareader


def print_links(data):
    for name, link in sorted(data.items(), key=lambda i: i[0]):
            print name, link


def main():
    search = sys.argv[1] if len(sys.argv) > 1 else None
    index = mangareader.get_manga_index()
    if not search:
        print_links(index)

    url = index.get(search)

    if not url:
        print search, 'Not found!!!'
        return

    print search, url

    chapters_index = dict(mangareader.get_manga_chapters(
        url, search))

    chapters = map(int, sys.argv[2:])
    if len(chapters) == 2:
        chapters = range(*chapters)

    print 'download chapters', chapters

    for c_id in chapters:
        print c_id, chapters_index[c_id]
        mangareader.get_chapter(search, c_id, chapters_index[c_id])
    # print_links(chapters)


main()
