#!/bin/bash
pytest --cov-config=.coveragerc --cov-branch -v --cov-report term-missing --cov=. -v . $1 $2
