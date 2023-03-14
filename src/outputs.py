import csv
import datetime as dt
import logging
from typing import Any, List, Tuple, Type, Union

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT


def control_output(
    results: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
    cli_args: Any
) -> None:
    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(
    results: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
) -> None:
    for row in results:
        print(*row)


def pretty_output(
    results: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
) -> None:
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(
    results: Union[List[Tuple[str, str]], List[Tuple[str, str, str]]],
    cli_args: Type[Any]
) -> None:
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    print(f'The file has been saved:{file_path}')
    logging.info(f'The file has been saved:{file_path}')
