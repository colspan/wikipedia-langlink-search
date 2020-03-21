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
CREATE TABLE `page` (
  `page_id` int(8) NOT NULL PRIMARY KEY,
  `page_title` varbinary(255)
  );
""",
]

try:
    for table_def in table_defs:
        c.execute(table_def)
except sqlite3.Error as e:
    print(e, 'skip create table')

re_exp = r'\(([0-9]+),[0-9]+,\'([\w\d_,]+)\','
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if i < skip_lines:
            continue
        records = re.findall(re_exp, line)
        for record in records:
            if len(record) != 2:
                continue
            id, title = record
            try:
                c.execute("INSERT INTO page VALUES (?,?)",
                          (id, title))
                pass
            except sqlite3.Error as e:
                print(e, record)

conn.commit()
conn.close()
