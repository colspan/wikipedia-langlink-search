#!/bin/sh

set -e

jawiki_dump=var/jawiki-latest-langlinks.sql
jawiki_db=var/jawiki-db.sqlite

skip_lines=$(expr $(grep -n INSERT ${jawiki_dump} | head -n 100 | cut -d ":" -f 1 | head -n 1) - 1)

scripts/extract_jawiki_langlinks.py ${jawiki_dump} ${jawiki_db} ${skip_lines}
