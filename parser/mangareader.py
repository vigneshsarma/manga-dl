import os
import re
import utils

from .decorators import cached_index

name = 'mangareader'
site = "http://www.%s.net" % name
site_index = site + "/alphabetical"


index_name = utils.index_location_format % (name)
site_folder = "%s%s/" % (utils.config_dir, name)


@cached_index(name)
def get_index():
    soup = utils.get_parsed(site_index)
    index = {}
    divs = soup.find_all("div", {"class": "series_alpha"})
    for div in divs:
        for link in div.find_all('a'):
            url = link.get('href')
            if url and url.startswith('/') and len(url) > 1:
                index[link.string] = url
    return index


def get_chapters(url, name):
    chapters_index_name = utils.index_location_format % re.sub(
        r'[ -/]', '_', name.lower())
    chapters = utils.get_index_from_store(site_folder, chapters_index_name)
    if chapters:
        return {int(chapter): url for chapter, url in chapters.items()}

    soup = utils.get_parsed(site + url)
    div = soup.find(id='chapterlist')
    chapters = {}
    for link in div.find_all('a'):
        url = link.get('href')
        if url and url.startswith('/') and len(url) > 1:
            chapters[int(link.string.replace(name, '').strip())] = url

    utils.store_index(chapters, site_folder, chapters_index_name)
    return chapters


def get_single_chapter(name, chapter, url):
    folder = os.path.join(name.replace(' ', '_'), "ch{}".format(chapter))
    utils.mkdir_p(folder)
    for page, img in _get_pages(url):
        utils.download_page(folder, page, img)
    print 'making cbz for', folder
    # utils.make_cbz(folder, delete_folder=False)


def _get_pages(start_page_url):
    count = 1
    soup = utils.get_parsed(site + start_page_url)
    img = soup.find("img")['src']
    next_page = soup.find('span', {'class': 'next'}).findChild()['href']
    yield count, img
    while next_page.startswith(start_page_url):
        print count,
        count += 1
        soup = utils.get_parsed(site + next_page)
        img = soup.find("img")['src']
        next_page = soup.find('span', {'class': 'next'}).findChild()['href']
        yield count, img
