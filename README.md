books
=====

This is a script for looking up ISBNs in the Google Books API, for the
purpose of building an inventory of a book collection.

Before using it, run `poetry install` and put your Google API key in
`.env` like this:

    KEY=<your api key>

The present workflow is

- scan the barcodes for all books from a given box with [Binary Eye](https://github.com/markusfisch/BinaryEye)
- share the scanned barcodes via email; before sending the message,
- manually enter the ISBNs for books that do not have barcodes
- take photographs of title pages of books that do not have ISBNs
- attach photos and send the email.

On receipt of the email, copy the barcodes into a file, `<box
number>.txt`, and use the code in this repo to do the lookup:

    ./books.sh <box number>

This will produce `<box number>.log` and `<box number>.csv`.
