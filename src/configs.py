import argparse
import errno
import logging
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from typing import Any

from constants import LOG_DIR, LOG_FILE_NAME
from enums.choices_for_parser import ParserMode, ParserOutput

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_argument_parser(available_modes: Any) -> ArgumentParser:
    parser = argparse.ArgumentParser(description='Python documentation parser')
    parser.add_argument(
        'mode',
        choices=ParserMode.modes(),
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        # choices=('pretty', 'file'),
        choices=ParserOutput.choices(),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging() -> None:
    try:
        LOG_DIR.mkdir(exist_ok=True)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    LOG_DIR.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE_NAME, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
