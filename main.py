#!/usr/bin/env python -u
import sys

from parser import mangareader, utils, hellocomic  # noqa

repo = hellocomic


def print_links(data):
    for name, link in sorted(data.items(), key=lambda i: i[0]):
            print name, link


def main():
    search = sys.argv[1] if len(sys.argv) > 1 else None
    index = repo.get_index()
    if not search:
        print_links(index)

    url = index.get(search)

    if not url:
        print search, 'Not found!!!'
        return

    print search, url

    chapters_index = dict(repo.get_chapters(
        url, search))

    chapters = map(int, sys.argv[2:])
    if len(chapters) == 2:
        file_name = 'ch{}-ch{}'.format(chapters[0], chapters[1]-1)
        chapters = range(*chapters)

    print 'download chapters', chapters

    for c_id in chapters:
        print c_id, chapters_index[c_id]
        repo.get_single_chapter(search, c_id, chapters_index[c_id])

    master_folder = search.replace(' ', '_') + '/'
    utils.make_cbz_with_many(
        file_name, ["%sch%d" % (master_folder, c_id) for c_id in chapters],
        delete_folder=True)
    # print_links(chapters)


main()
