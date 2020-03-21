#!/usr/bin/env python
import argparse
import csv
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('titles', metavar='N', type=str, nargs='+',
                    help='list of titles')
parser.add_argument('--output', type=str)
parser.add_argument("--database", default='var/jawiki-db.sqlite')
args = parser.parse_args()

conn = sqlite3.connect(args.database)

c = conn.cursor()

query = """
select p.id, p.title, l.lang, l.title from langlinks as l
    join (select page.id, page.title from page where page.title=? ) as p
    on p.id=l.id;
"""
records = []
langcodes = ['jp']
for title in args.titles:
    record = {
        'jp': title,
    } 
    for row in c.execute(query, [title]):

        _, _, langcode, transtitle = row
        record[langcode] = transtitle
        langcodes.append(langcode)
    records.append(record)
conn.close()

fieldnames = sorted(list(set(langcodes)))

with open(args.output, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames,delimiter=",",quotechar='"')
    writer.writeheader()
    for record in records:
        writer.writerow(record)

