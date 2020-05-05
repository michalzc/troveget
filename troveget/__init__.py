"""trove-get

Usage:
    trove-get <trove-url> [<output-dir>]
"""

import os.path
import sys
from logging import getLogger
from pathlib import PurePosixPath
from urllib.parse import unquote_plus, urlparse

from docopt import docopt

from troveget.utils import get_dir_from_url

logger = getLogger('trove-get')
    

def check_args(arguments):
    out_dir = arguments['<output-dir>'] or '.'
    if os.path.exists(out_dir) and not os.path.isdir(out_dir):
        logger.error("%s exist and is not a directory", out_dir)
        sys.exit(1)

    url = arguments['<trove-url>']
    if not url.startswith('https://'):
        url = 'https://' + url
    if url.endswith('/index.html'):
        url = url.replace('/index.html', '/')
    if not url.startswith('https://thetrove.net/'):
        logger.error("%s is not supported", url)
        sys.exit(1)
    if not url.endswith('/'):
        url = url + '/'

    out_dir = arguments['<output-dir>'] or get_dir_from_url(url)
    if os.path.exists(out_dir) and not os.path.isdir(out_dir):
        logger.error("%s exist and is not a directory", out_dir)
        sys.exit(1)        

    return (url, out_dir)



def get():
    arguments = docopt(__doc__, version='trove-get 0.1')
    url, out_dir = check_args(arguments)
    print("Params: ", url, out_dir)
