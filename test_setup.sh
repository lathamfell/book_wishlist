#!/bin/sh
docker stop booklist
docker rm booklist
docker build -t booklist .
docker run --name booklist booklist &
