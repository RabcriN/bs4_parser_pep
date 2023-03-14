import logging
from typing import Any, Optional, Type
from requests import Response  # type: ignore

from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session: Type[Any], url: str) -> Optional[Response]:
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'An error occurred while loading the page {url}',
            stack_info=True
        )
    return None


def find_tag(soup: Type[Any], tag: str, attrs=None) -> Type[Any]:
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
