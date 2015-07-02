import os
import time
import json
import errno
import shutil
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup

config_dir = os.path.expanduser('~') + '/.manga-dl/'

index_location_format = "%s.index.json"


def store_index(index, dir_name, file_name):
    mkdir_p(dir_name)
    with open(dir_name + file_name, 'w') as f:
        json.dump(index, f, indent=2)


def get_index_from_store(dir_name, file_name):
    path = dir_name + file_name
    if not os.path.exists(path):
        return False
    one_day = 60 * 60 * 24
    if time.time() - os.path.getmtime(path) > one_day:
        return False
    with open(path) as f:
        return json.load(f)


def download_page(folder, page, img_url):
    local_filename = os.path.join(folder, "{}.jpg".format(page))
    r = requests.get(img_url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def make_cbz(folder, delete_folder=False):
    with ZipFile(folder + '.cbz', mode='w') as cbz:
        for page in os.listdir(folder):
            cbz.write(os.path.join(folder, page))

    if delete_folder:
        shutil.rmtree(folder)


def get_parsed(url):
    return BeautifulSoup(requests.get(url).content)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
