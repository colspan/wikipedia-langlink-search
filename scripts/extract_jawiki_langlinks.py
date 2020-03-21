#!/usr/bin/env python
import sys
import sqlite3

filepath = sys.argv[1]
output_db_path = sys.argv[2]
skip_lines = int(sys.argv[3])

conn = sqlite3.connect(output_db_path)
c = conn.cursor()

table_defs = [
    """
CREATE TABLE `langlinks` (
  `ll_from` int(8)  NOT NULL,
  `ll_lang` varbinary(20),
  `ll_title` varbinary(255));
""",
    """
CREATE INDEX idx_langlinks_fromlang 
ON langlinks (ll_from, ll_lang);
"""
]

try:
    for table_def in table_defs:
        c.execute(table_def)
except sqlite3.Error as e:
    print(e, 'skip create table')

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if i < skip_lines:
            continue
        records = line.split('(')
        for record in records[1:]:
            values = record.replace('),', '').split(',')
            if len(values) != 3:
                continue
            id = values[0]
            lang = values[1]
            title = values[2].replace("'", '')

            try:
                c.execute("INSERT INTO langlinks VALUES (?,?,?)",
                          (id, lang, title))

            except sqlite3.Error as e:
                print(e, values)

conn.commit()
conn.close()
