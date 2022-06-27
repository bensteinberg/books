#!/bin/bash

BOX=$1

poetry run python books.py --box $BOX --headings < $BOX.txt > $BOX.csv 2> $BOX.log
