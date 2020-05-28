# Book Wishlist
Keeps a wishlist of books to read.  Supports CRUD operations on books, users, and wishlists.

# Design
The wishlist service is deployed inside a container.  The wishlist data is maintained in a SQLite database located inside the running container.  When the container stops, the data is lost.

The REST API is implemented in Flask and provides endpoints to perform Create, Read, Update and Delete operations on books, users, and wishlists.  When a book is deleted, it is removed from all wishlists.  When a user is deleted, their wishlist is also deleted.  User passwords are encrypted in the database.  User passwords are not used anywhere.

Gunicorn is used as the WSGI, since the native Flask WSGI is not suitable for production loads.

The "cookiecutter" Flask implementation (https://github.com/cookiecutter-flask/cookiecutter-flask) is used, which eliminates several issues often encountered when using Flask.  These include the circular import issue, testing environment separation issues, and logging conflicts.
The database interface is implemented as a dedicated module (db_interface.py), so that switching databases would be as easy as replacing that module.

Some inspiration for the SQL commands used in this service came from Ryan Nowacoski's Book API service: https://github.com/rmn36/book_api

# Database schema
There is a table for books, and a table for users.  There is also table called "Lists" with two columns: user_email and isbn.  A user's wishlist consists of all rows in the Lists table that have their unique email.

# Dependencies
Docker

# Execution
Execute
`docker build -t booklist .`
`docker run -p 8000:8000 booklist`

# Commands
This a complete set of available API requests, and can be executed in order to demonstrate the service's functionality.

Create user:
`curl -d '{"first_name": "Latham", "last_name": "Fell", "email": "me@me.com", "password": "1234"}' -H "Content-Type: application/json" -X POST http://localhost:8000/add_user`

Get data for a particular user:
`curl http://localhost:8000/get_user?email=me@me.com`

Create book:
`curl -d '{"title": "Tiamats Wrath", "author": "James S. Corey", "isbn": "978-3-16-148410-0", "pub_date": "2020-03-24"}' -H "Content-Type: application/json" -X POST http://localhost:8000/add_book`

Get data for a particular book:
`curl http://localhost:8000/get_book?isbn=978-3-16-148410-0`
`curl http://localhost:8000/get_book?isbn=12345`

Add book to user wishlist (book and user must already have been created):
`curl -d '{"email": "me@me.com", "isbn": "978-3-16-148410-0"}' -H "Content-Type: application/json" -X POST http://localhost:8000/add_book_to_list`
`curl -d '{"email": "me@me.com", "isbn": "12345"}' -H "Content-Type: application/json" -X POST http://localhost:8000/add_book_to_list`

Get a wishlist:
`curl -X GET http://localhost:8000/get_list?email=me@me.com`

Update a user (user associated with provided email will have its attributes changed to those provided):
`curl -d '{"email": "me@me.com", "first_name": "Nancy", "last_name": "Drew"}' -H "Content-Type: application/json" -X POST http://localhost:8000/update_user`

Update a book (book with provided isbn will have its attributes changed to those provided):
`curl -d '{"title": "Grapes of Wrath", "author": "James Gunn", "isbn": "978-3-16-148410-0"}' -H "Content-Type: application/json" -X POST http://localhost:8000/update_book`

Remove book from a wishlist:
`curl -d '{"email": "me@me.com", "isbn": "978-3-16-148410-0"}' -H "Content-Type: application/json" -X POST http://localhost:8000/remove_book_from_list`

Delete book (also removes from all wishlists):
`curl -d '{"email": "me@me.com", "isbn": "12345"}' -H "Content-Type: application/json" -X POST http://localhost:8000/delete_book`

Delete user (also removes the user's wishlist):
`curl -d '{"email": "me@me.com"}' -H "Content-Type: application/json" -X POST http://localhost:8000/delete_user`


# Test
`./test_setup.sh`
Press Enter
`docker exec -it booklist ./test.sh`
`./test_teardown.sh`

## Test database

The tests are configured to use a dedicated test database, which allows the tests to be run in the container right alongside the live service.  Even in production, if desired!

# Scaling up
The service is containerized, so it may be run on Kubernetes (K8s) and scaled up/down based on demand.  To conserve resources, a compact Alpine Docker image should be used instead of the current full Python image.

The database will need to be moved out of the container and persisted somewhere, such as in AWS RDS.  There, read replicas and, if necessary, write replicas can be created based on demand.  The ratio of reads to writes is likely to be something on the order of 10:1.  This is based on the assumption that users will view their wishlists often, but make changes to them less frequently.

A load balancer/reverse proxy, such as nginx, will need to be used in the K8s to allocate requests across pods.  Once the database is moved out of the container, the pods will have no state.  Any pod can handle a request.  If the number of requests leads to excessive transaction locks in the database, a switch to a NoSQL database could be considered.  This depends on how important it is that a change to a user's wishlist be reflected on all read replicas before any other reads/writes occur.

To increase availability and response time, the service should be implemented in multiple AWS regions.  If a user request could not be served by a region service, it would query a central service.  That data could then be cached in the region to increase responsiveness, and possibly migrated permanently to a region if indications are that the user has permanently changed locations.
