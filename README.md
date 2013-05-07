# libpuzzle DEMO

This a sample website of PyPuzzle(a Python module based on libpuzzle).

It illustrate how to:

1. build the SQL schema and how to index millions of images.

1. find a similar image from database quickly.

## How to use:

1. `$ sqlite3 db/puzzle.db`.
1. `$ python init_db.py`.
1. `$ python app.py` and open '127.0.0.1:5000' in browser.

## TODO

1. manage dependences with virtualenv.
2. search by description. (done)