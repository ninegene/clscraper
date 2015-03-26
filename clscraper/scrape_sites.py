import logging
from conf import CACHE_DIR, CL_SITES_URL
from utils import get_content
from bs4 import BeautifulSoup
import re

log = logging.getLogger(__name__)


def scrape_sites():
    content = get_content(CL_SITES_URL, CACHE_DIR)
    soup = BeautifulSoup(content)

    tags = soup.find('div', class_='jump_to_continents').find_all('a')

    for tag in tags:
        name = tag.text
        anchor = re.sub(r'^#', '', tag.get('href'))
        _process_continent(soup, name, anchor)

    log.info('done scrape_sites')


def _process_continent(soup, continent, anchor):
    sites = []
    h1 = soup.find('a', attrs={'name': anchor}).find_parent('h1')
    div = h1.next_sibling.next_sibling
    tags = div.find_all('h4')
    for tag in tags:
        country = tag.text
        links = tag.next_sibling.next_sibling.find_all('a')
        for link in links:
            site = link.text
            site_link = link['href']
            data = {
                'continent_key': anchor,
                'continent': continent,
                # US and Canada have states
                'country': continent if anchor == 'US' or anchor == 'CA' else country,
                'state': country if anchor == 'US' or anchor == 'CA' else None,
                'site': site,
                'site_link': site_link
            }
            log.debug(data)
            sites.append(data)


if __name__ == '__main__':
    scrape_sites()