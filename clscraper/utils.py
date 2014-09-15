from datetime import datetime
from hashlib import sha1
import os
import logging

log = logging.getLogger(__name__)


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def mkdir(path, mode=0777):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path, mode)
    return path


def to_hash(str):
    return sha1(str).hexdigest()


def current_timestr(cur=None):
    cur = cur or datetime.now()
    return cur.strftime("%Y-%m-%d-%H%M%S")


def to_html_fname(url, created_at=None):
    digest = to_hash(url)
    if created_at:
        timestr = current_timestr(created_at)
        return timestr + '_' + digest + '.html'
    return digest + '.html'


def to_html_fpath(url, base_dir, created_at=None):
    return os.path.join(base_dir, to_html_fname(url, created_at))


def saveas_html(url, content, basedir, created_at=None):
    mkdir(basedir)

    path = to_html_fpath(url, basedir, created_at)
    with open(path, 'wb') as f:
        f.write(content)
    log.info('saved ' + url + ' to ' + path)
    return path


def load_html(url, basedir, created_at=None):
    path = to_html_fpath(url, basedir, created_at)
    if not os.path.exists(path):
        return None

    with open(path, 'rb') as f:
        content = f.read()
    log.info('loaded ' + url + ' from ' + path)
    return content


def append_url_to_content(url, content):
    return content + '\n<!--source_url: {0}-->'.format(url)