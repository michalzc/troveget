"""trove-get

Usage:
    trove-get [-n | --no-follow] <trove-url> [<output-dir>]

Options:
    -h --help       Show this screen
    -n --no-follow  Do not step down into directories
"""

import os
import os.path
import sys
import posixpath
from logging import getLogger, basicConfig
from pathlib import PurePosixPath
from urllib.parse import unquote_plus, urlparse

from docopt import docopt

from troveget.utils import get_dir_from_url
from troveget.trovedownload import download_page, download_file
from troveget.troveparse import find_links

basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = getLogger('trove-get')
    

def check_args(arguments):
    out_dir = arguments.get('<output-dir>') or '.'
    if os.path.exists(out_dir) and not os.path.isdir(out_dir):
        logger.error("%s exist and is not a directory", out_dir)
        sys.exit(1)

    url = arguments.get('<trove-url>')
    if not url.startswith('https://'):
        url = 'https://' + url
    if url.endswith('/index.html'):
        url = url.replace('/index.html', '/')
    if not url.startswith('https://thetrove.net/'):
        logger.error("%s is not supported", url)
        sys.exit(1)
    if not url.endswith('/'):
        url = url + '/'

    out_dir = arguments.get('<output-dir>') or get_dir_from_url(url)
    if os.path.exists(out_dir) and not os.path.isdir(out_dir):
        logger.error("%s exist and is not a directory", out_dir)
        sys.exit(1)

    no_follow = arguments.get('--no-follow') or False

    return (url, out_dir, no_follow)

def check_directory(out_dir):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    elif not os.path.isdir(out_dir):
        logger.error("%s exists and it's not a directory", out_dir)
        sys.exit(1)    


def run(url, out_dir, no_follow):
    logger.info("Processing %s page, download dir %s", url, out_dir)
    check_directory(out_dir)
    page_source = download_page(url)
    if page_source:
        page_links, file_links = find_links(page_source)
        for fl in file_links:
            file_url = posixpath.join(url, fl)
            download_file(file_url, out_dir)

        for pl in page_links and not no_follow:
            page_url = posixpath.join(url, pl)
            page_out_dir = os.path.join(out_dir, get_dir_from_url(page_url))
            run(page_url, page_out_dir, no_follow)

    else:
        logger.warn("No data for %s, skipping", url)
        


def get():
    arguments = docopt(__doc__, version='trove-get 0.1')
    url, out_dir, no_follow = check_args(arguments)
    run(url, out_dir, no_follow)
