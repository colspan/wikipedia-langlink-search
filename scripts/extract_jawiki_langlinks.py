#!/usr/bin/env python
import re
import sqlite3
import sys

filepath = sys.argv[1]
output_db_path = sys.argv[2]
skip_lines = int(sys.argv[3])

conn = sqlite3.connect(output_db_path)
c = conn.cursor()

table_defs = [
    """
CREATE TABLE `langlinks` (
  `ll_from` int(8) NOT NULL,
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

re_exp = r'\(([0-9]+),\'([\w\d_,]+)\',\'([\w\d_,]+)\'\)'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if i < skip_lines:
            continue
        records = re.findall(re_exp, line)
        for record in records:
            if len(record) != 3:
                continue
            id, lang, title = record

            try:
                c.execute("INSERT INTO langlinks VALUES (?,?,?)",
                          (id, lang, title))

            except sqlite3.Error as e:
                print(e, record)

conn.commit()
conn.close()
