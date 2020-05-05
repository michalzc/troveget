import os.path
from logging import getLogger

import requests
from tqdm import tqdm

from troveget.utils import get_dir_from_url

MEGA = 1024 * 1024

logger = getLogger(__file__)

def download_file(url, base_dir=None):
    dest_name = get_dir_from_url(url)
    dest = base_dir and os.path.join(base_dir, dest_name) or dest_name

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        logger.info("%s - request successful, downloading", url)
        rl = response.headers.get('Content-Length')
        response_length = rl and int(rl) or None
        with tqdm(total=response_length, desc='Downloading %s' % dest_name, unit='bytes') as pbar:
            with open(dest, 'wb') as fl:
                for chunk in response.iter_content(chunk_size=MEGA):
                    writen = fl.write(chunk)
                    pbar.update(writen)
    else:
        logger.warn("Can't download %s, response status ->  %d", url, response.status_code)
        logger.warn(response.content)


def download_page(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        logger.info("Successfuly get page %s", url)
        return resp.content.decode('utf-8')
    else:
        logger.warn("Can't get the %s page, response status -> %d", url, resp.status_code)
        logger.warn(resp.content.decode('utf-8'))
        return None