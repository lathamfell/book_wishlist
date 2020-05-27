# book_wishlist
Keeps a wishlist of books to read

# Dependencies
Docker

# Execution
Execute
`docker build -t booklist .`
`docker run -p 8000:8000 booklist`

# Commands
Create user wishlist:
`curl -d '{"first_name": "Latham", "last_name": "Fell", "email": "me@me.com", "password": "1234"}' -H "Content-Type: application/json" -X PUT http://localhost:8000/add_user`

Get a wishlist:
`curl -X GET http://localhost:8000/get_list?email=me@me.com`

Update a user wishlist (user list associated with provided email will have its attributes changed to those provided):
`curl -d '{"email": "me@me.com", "first_name": "Nancy", "last_name": "Drew"}' -H "Content-Type: application/json -X POST http://localhost:8000/update_user`

Delete user wishlist:
`curl -d '{"email": "me@me.com"}' -H "Content-Type: application/json" -X POST http://localhost:8000/delete_user`

Create book:
`curl -d '{"title": "Tiamat's Wrath", "author": "James S. Corey", "isbn": "12345", "pub_date": "2020-03-24"}' -H "Content-Type: application/json" -X POST http://localhost:8000/add_book`

Delete book (also removes from all wishlists):
`curl -d '{"email": "me@me.com", "isbn": "12345"} -H "Content-Type: application/json -X POST http://localhost:8000/delete_book`

Update book (book with provided isbn will have its attributes changed to what is included):
`curl -d '{"title": "Grapes of Wrath", "author": "James Gunn", "isbn": "12345", "pub_date": "2020-03-24"}' -H "Content-Type: application/json" -X POST http://localhost:8000/update_book`

Add book to user wishlist (book and user must already have been created):
`curl -d '{"email": "me@me.com", "isbn": "12345"}' -H "Content-Type: application/json" -X POST http://localhost:8000/add_book_to_list`

Remove book from a wishlist:
`curl -d '{"email": "me@me.com", "isbn": "12345"} -H "Content-Type: application/json" -X POST http://localhost:8000/remove_book/`


# Test
`./test_setup.sh`
Press Enter
`docker exec -it booklist ./test.sh`
`./test_teardown.sh`
