# Data Pipeline — Book Catalog

## Objective

This module implements a complete data-engineering pipeline:

Scrape → Clean → Convert → Store → Query → Validate

The source is Books to Scrape, a public website designed for scraping
practice.

Source:
https://books.toscrape.com/

## Scraping Scope

The pipeline scrapes one listing page from each of three categories:

- Mystery
- Young Fiction
- Default

Each category contributes 20 books, producing at least 60 books across
3 categories.

The scraping is performed programmatically using:

- requests
- BeautifulSoup

No manual copy-pasting is used.

## Data Cleaning

### Price

The GBP currency symbol is removed and the value is converted to float.

Column:

price_gbp

### Rating

Text ratings are converted as follows:

One = 1
Two = 2
Three = 3
Four = 4
Five = 5

Column:

rating

### Availability

Availability text is converted to boolean:

In stock = True
Out of stock = False

SQLite stores the boolean as:

1 = True
0 = False

Column:

in_stock

### Parsing failures

Numeric parsing failures are handled using median imputation.

For invalid availability values, the affected row is dropped because
median imputation is not meaningful for a boolean field.

The pipeline therefore does not crash because of an individual malformed row.

## Currency Conversion

The required project-defined fixed conversion rate is:

1 GBP = 105.50 INR

This is an artificial fixed baseline for the assignment.

No live exchange-rate API is used.

price_inr is calculated as:

price_inr = price_gbp * 105.50

The result is rounded to two decimal places.

## Database Design

A normalized SQLite database is used.

### categories

- category_id INTEGER PRIMARY KEY
- category_name TEXT UNIQUE NOT NULL

### books

- book_id INTEGER PRIMARY KEY
- title TEXT NOT NULL
- price_gbp REAL NOT NULL
- price_inr REAL NOT NULL
- rating INTEGER NOT NULL
- in_stock INTEGER NOT NULL
- category_id INTEGER FOREIGN KEY

Relationship:

books.category_id → categories.category_id

The category name is stored once in the categories table instead of being
repeated for every book.

## SQL Queries

Five SQL queries are executed.

1. SELECT + WHERE + BETWEEN + ORDER BY
2. ORDER BY + LIMIT
3. DISTINCT + JOIN
4. IN + ORDER BY
5. JOIN to identify highest-rated books per category

The SQL query strings and their outputs are saved in:

outputs/query_outputs.txt

## Pandas Validation

The JOIN query is reproduced in pandas using:

pd.merge()

The SQL result is read using:

pd.read_sql()

Both results are compared using DataFrame.equals().

The comparison output is saved in:

outputs/pandas_comparison.txt

The expected comparison result is:

Equivalent: True

## Generated Files

- books_catalog.db
- outputs/cleaned_books.csv
- outputs/query_outputs.txt
- outputs/pandas_comparison.txt

## Running the Pipeline

Install dependencies:

pip install requests beautifulsoup4 pandas

Then run the notebook or Python scraping script.

The pipeline recreates the SQLite database from the source data.

## Git Requirement

The repository must contain:

- a feature branch
- at least two commits on that feature branch
- a merge back into main

Example:

git checkout -b feature/data-pipeline

git add data_pipeline
git commit -m "feat: add catalog scraping and cleaning"

git add data_pipeline
git commit -m "feat: add SQLite schema and SQL validation"

git checkout main
git merge --no-ff feature/data-pipeline -m "merge: data pipeline module"

Verify with:

git log --oneline --graph --decorate --all