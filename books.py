import click
import os
from dotenv import load_dotenv
import requests
import csv
import sys
import logging


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.INFO)


@click.command()
@click.option('--isbn', help='A single ISBN')
@click.option('--box', help='Box number or other location')
@click.option('--headings/--no-headings', default=False,
              help='Add headings to CSV output')
@click.option('--verbose/--no-verbose', default=False,
              help='Log full responses')
def lookup(isbn, box, headings, verbose):
    """Look up book information for one or more ISBNs."""
    # get the Google API key from the environment, not options (?)
    load_dotenv()
    key = os.getenv('KEY')

    route = 'https://www.googleapis.com/books/v1/volumes'

    if isbn:
        isbns = [isbn]
    else:
        isbns = []
        stream = click.get_text_stream('stdin')
        for line in stream.readlines():
            isbns.append(line.strip())

    cleaned = list(set([clean(i) for i in isbns]))
    if len(cleaned) < len(isbns):
        logging.warning('Found duplicates')
    logging.info(f'Searching {len(cleaned)} ISBNs')
    logging.info(f'{isbns}')

    fieldnames = ['gbid', 'isbn', 'authors', 'title',
                  'publisher', 'pubdate', 'box']
    writer = csv.writer(sys.stdout)
    if headings:
        writer.writerow(fieldnames)

    for c in cleaned:
        if len(c) not in [10, 13]:
            logging.warning(f'Length of {c} is not 10 or 13')
            continue

        query = f'q=isbn:{c}&key:{key}'
        url = f'{route}?{query}'

        r = requests.get(url)
        response = r.json()

        if verbose:
            logging.info(response)

        items = response['totalItems']
        if items == 0:
            logging.warning(f'No response for {c}')
            continue
        elif items > 1:
            logging.warning(f'Multiple results for {c}')

        for volume in range(items):
            gbid = response['items'][volume]['id']
            info = response['items'][volume]['volumeInfo']
            title = info.get('title')
            try:
                authors = ', '.join(info.get('authors'))
            except TypeError:
                authors = info.get('authors')
            publisher = info.get('publisher')
            pubdate = info.get('publishedDate')
            row = [gbid, c, authors, title, publisher, pubdate, box]
            assert len(row) == len(fieldnames)
            writer.writerow(row)


def clean(isbn):
    '''
    This might well check ISBNs for correctness, but this will do for now.
    '''
    return ''.join(c for c in isbn if c.isalnum())


if __name__ == '__main__':
    lookup()
