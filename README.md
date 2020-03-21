# wikipedia-langlink-search

## Prepare Database

```bash
scripts/fetch-jawiki-langlinks.sh
scripts/prepare-jawiki-langlinks.sh

scripts/fetch-jawiki-page.sh
scripts/prepare-jawiki-page.sh
```

## Search by SQLite

```sql
select p.id, p.title, l.lang, l.title from page as p join langlinks as l on p.id=l.id;

select p.id, p.title, l.lang, l.title from langlinks as l join (select page.id, page.title from page where page.title='札幌市' ) as p on p.id=l.id;
```

## Search by example script

```bash
python examples/get_titles_csv.py 北海道 札幌市 函館市 旭川
市 釧路市 北見市 帯広市 稚内市 --output var/hokkaido.csv
```
