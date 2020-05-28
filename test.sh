#!/bin/sh
export DB_NAME="booklist_test.db"
pytest --cov-config=.coveragerc --cov-branch -v --cov-report term-missing --cov=. -v . $1 $2
