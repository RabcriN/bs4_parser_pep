import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_URL
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')

    response = get_response(session, whats_new_url)
    if response is None:
        return

    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]

    for section in tqdm(
            sections_by_python,
            desc='Pages parsing progress:',
            ncols=100,
            ):
        version_a_tag = section.find('a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])

        response = get_response(session, version_link)
        if response is None:
            continue

        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        dl_text = dl_text[:7] + ':' + dl_text[7:]
        results.append(
            (
                version_link,
                h1.text[:-1],
                dl_text,
            )
        )
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return

    soup = BeautifulSoup(response.text, features='lxml')
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All version' in ul.text:
            a_tags = ul.find_all('a')
            break
        else:
            raise Exception('Python version list has not found')

    results = [('Link', 'Version', 'Status')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text = (a_tag.text)
        text_match = re.search(pattern, text)
        try:
            version, status = (text_match.group('version', 'status'))
        except AttributeError:
            version, status = text, ''
        results.append((link, version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return

    soup = BeautifulSoup(response.text, features='lxml')
    table_tag = find_tag(soup, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)

    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    print(f'You can find your downloaded file here: {archive_path}')
    logging.info(f'You can find your downloaded file here: {archive_path}')


def pep(session):
    response = get_response(session, PEP_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    pep_by_index = find_tag(soup, 'section', {'id': 'numerical-index'})
    body = find_tag(pep_by_index, 'tbody')
    tr_tags = body.find_all('tr')
    status_counter = dict()
    for tag in tqdm(
            tr_tags,
            desc='PEP parsing progress:',
            ncols=100,
            ):
        tag_link = find_tag(tag, 'a')
        status = find_tag(tag, 'abbr').text[1:]

        pep_link = urljoin(PEP_URL, tag_link['href'])
        new_response = get_response(session, pep_link)
        new_soup = BeautifulSoup(new_response.text, features='lxml')
        link_content = find_tag(new_soup, 'section', {'id': 'pep-content'})
        link_dl_tag = find_tag(link_content, 'dl')
        link_dt_status = link_dl_tag.find(
            lambda tag: tag.name == 'dt' and 'Status' in tag.text
            )
        link_status = link_dt_status.findNext('dd').text
        if link_status not in EXPECTED_STATUS[status]:
            logging.info(
                f'Mismatched statuses! Link: {pep_link} '
                f'Status in PEP list: {status} '
                f'Expected status: {EXPECTED_STATUS[status]} '
                f'Status on PEP page = {link_status}'
            )
        if link_status not in status_counter.keys():
            status_counter[link_status] = 1
        else:
            status_counter[link_status] += 1
    results = [('Status', 'Quantity')]
    total = 0
    for key, value in status_counter.items():
        results.append((key, value))
        total += value
    results.append(('Total: ', total))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Parser has been started!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Cli args: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('The program has been finished.')


if __name__ == '__main__':
    main()
