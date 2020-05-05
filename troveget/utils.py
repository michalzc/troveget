from pathlib import PurePosixPath
from urllib.parse import unquote_plus, urlparse

def get_dir_from_url(url):
    return PurePosixPath(
        unquote_plus(
            urlparse(url).path
        )
    ).parts[-1]