import os
import re
import utils

from .decorators import cached_index

name = 'hellocomic'
site = 'http://www.%s.com/' % name
naked_site = 'http://%s.com/' % name
site_index = site + 'comic/list'

index_name = utils.index_location_format % (name)
site_folder = "%s%s/" % (utils.config_dir, name)


@cached_index(name)
def get_index():
    soup = utils.get_parsed(site_index)
    index = {}
    links = soup.find_all("a", {"class": "popupLink"})
    for link in links:
        url = link.get('href')
        index[link.string] = url
    return index


def get_chapters(url, name):
    chapters_index_name = utils.index_location_format % re.sub(
        r'[ -/]', '_', name.lower())
    chapters = utils.get_index_from_store(site_folder, chapters_index_name)
    if chapters:
        return {int(chapter): url for chapter, url in chapters.items()}

    soup = utils.get_parsed(url)
    links = soup.find('tbody').find_all('a')
    chapters = {}
    for link in links:
        url = link.get('href')
        if url and url.startswith(site) and len(url) > (len(site) + 1):
            chapters[int(link.string.replace(name + ' - #', '').strip())] = url

    utils.store_index(chapters, site_folder, chapters_index_name)
    return chapters


def get_single_chapter(name, chapter, url):
    folder = os.path.join(name.replace(' ', '_'), "ch{}".format(chapter))
    utils.mkdir_p(folder)
    for page, img in _get_pages(url):
        utils.download_page(folder, page, img)


def _get_pages(start_page_url):
    chapter_url = start_page_url.replace('/p1', '')
    count = 1
    soup = utils.get_parsed(start_page_url)
    img = _find_img(soup)
    next_page = soup.find('a', {'class': 'nextLink'})['href']
    yield count, img
    while next_page.startswith(chapter_url):
        print count,
        count += 1
        soup = utils.get_parsed(next_page)
        img = _find_img(soup)
        next_page = soup.find('a', {'class': 'nextLink'})['href']
        yield count, img


def _find_img(soup):
    for img in soup.find_all("img"):
        if img['src'].startswith(naked_site):
            return img['src']
