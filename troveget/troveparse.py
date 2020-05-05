import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def find_links(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    directory_links = []
    file_links = []
    for tr in soup.find_all('tr'):
        cl = tr.get('class')
        if cl and len(cl) == 2 and cl[0] == 'litem':
            classifier = cl[1]
            a = tr.find('a', draggable='true')
            href = a and a['href']
            if classifier == 'dir' and href and href != '../index.html':
                directory_links.append(href)
            elif classifier == 'file' and href:
                file_links.append(href)



    if directory_links:
        logger.debug("Directory links:")
        for l in directory_links:
            logger.debug("\t- %s", l)

    if file_links:
        logger.debug("File links:")
        for l in file_links:
            logger.debug("\t- %s", l)

    return(directory_links, file_links)