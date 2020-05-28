import pytest
import sqlite3
from app_files.config import constants
from app_files import db_helpers
import flask_settings


USER1 = {
    "first_name": "Roger",
    "last_name": "Blankman",
    "email": "roger@gmail.com",
    "password": "1234",
}
BOOK1 = {
    "title": "Tiamat's Wrath",
    "author": "James S. Corey",
    "isbn": "978-3-16-148410-0",
    "pub_date": "2020-03-24",
}


@pytest.fixture
def setup():
    db_helpers.clear_database()
    db_helpers.setup_database()
    setup = {}
    yield setup


def test_index(setup, testapp):
    res = testapp.get("/")
    assert res.status_code == 200
    assert res.json["status"] == "OK"

    res = testapp.get("/index")
    assert res.status_code == 200
    assert res.json["status"] == "OK"


def test_add_user(setup, testapp):
    res = testapp.post_json("/add_user", USER1, status=200)
    assert res.json["status"] == "User added"

    params = "?email=roger@gmail.com"
    res = testapp.get(f"/get_user{params}", status=200)
    assert res.json["status"] == "User returned"
    #assert res.text == '{"email":"roger@gmail.com"
    # TODO check user data


def test_get_list(setup, testapp):
    # create a list to be fetched
    testapp.post_json("/add_user", USER1, status=200)
    testapp.post_json("/add_book", BOOK1, status=200)
    testapp.post_json("/add_book_to_list", {"email": USER1["email"], "isbn": BOOK1["isbn"]})

    params = "?email=roger@gmail.com"
    res = testapp.get(f"/get_list{params}", status=200)
    assert res.json["status"] == "List returned"
    # TODO check list data


def test_get_user(setup, testapp):
    # create a user to be fetched
    testapp.post_json("/add_user", USER1, status=200)

    params = "?email=roger@gmail.com"
    res = testapp.get(f"/get_user{params}", status=200)
    # TODO check user data that it matches USER1


def test_update_user(setup, testapp):
    # create a user to be updated
    testapp.post_json("/add_user", USER1, status=200)

    res = testapp.post_json(
        "/update_user", {"email": "roger@gmail.com", "first_name": "Bob"}, status=200
    )

    assert res.json["status"] == "User updated"
    
    params = "?email=roger@gmail.com"
    res = testapp.get(f"/get_user{params}", status=200)
    # TODO check user data to see if first name changed to Bob


def test_delete_user(setup, testapp):
    # create a user to be deleted
    testapp.post_json("/add_user", USER1, status=200)

    res = testapp.post_json("/delete_user", {"email": "roger@gmailcom"}, status=200)

    assert res.json["status"] == "User deleted"

    #TODO res = testapp.get("/get_user", USER1, status=404)
    # TODO assert res.json["status"] == "User not found"


def test_add_book(setup, testapp):
    res = testapp.post_json("/add_book", BOOK1, status=200)
    assert res.json["status"] == "Book added"

    params = "?isbn=978-3-16-148410-0"
    res = testapp.get(f"/get_book{params}", status=200)
    # TODO check book data matches BOOK1


def test_get_book(setup, testapp):
    # create a book to be fetched
    testapp.post_json("/add_book", BOOK1, status=200)

    params = "?isbn=978-3-16-148410-0"
    res = testapp.get(f"/get_book{params}", status=200)
    assert res.json["status"] == "Book returned"
    # TODO check book data matches BOOK1


def test_update_book(setup, testapp):
    # create a book to be updated
    testapp.post("/add_book", BOOK1, status=200)

    res = testapp.post_json(
        "/update_book",
        {"isbn": "978-3-16-148410-0", "author": "Paul Patrick"},
        status=200,
    )
    assert res.json["status"] == "Book updated"
    # TODO test book author is now Paul Patrick


def test_delete_book(setup, testapp):
    # create a book to be deleted
    testapp.post_json("/add_book", BOOK1, status=200)

    res = testapp.post_json("/delete_book", {"isbn": "978-3-16-148410-0"}, status=200)

    assert res.json["status"] == "Book deleted"

    params = "?isbn=978-3-16-148410-0"
    # TODO res = testapp.get(f"/get_book{params}", status=404)
    # TODO assert res.json["status"] == "Book not found"


def test_add_book_to_list(setup, testapp):
    # create a book and a user
    testapp.post_json("/add_book", BOOK1, status=200)
    testapp.post_json("/add_user", USER1, status=200)

    res = testapp.post_json(
        "/add_book_to_list",
        {"email": "roger@gmail.com", "isbn": "978-3-16-148410-0"},
        status=200,
    )
    assert res.json["status"] == "Book added to list"

    res = testapp.get("/get_list", {"email": "roger@gmail.com"}, status=200)
    # TODO test book is on the list


def test_remove_book(setup, testapp):
    # create a list with a book to be removed
    testapp.post_json("/add_book", BOOK1, status=200)
    testapp.post_json("/add_user", USER1, status=200)
    testapp.post_json(
        "/add_book_to_list",
        {"email": USER1["email"], "isbn": BOOK1["isbn"]},
        status=200,
    )

    res = testapp.post_json(
        "/remove_book_from_list",
        {"email": USER1["email"], "isbn": BOOK1["isbn"]},
        status=200,
    )
    assert res.json["status"] == "Book removed from list"

    res = testapp.get("/get_list", {"email": USER1["email"]}, status=200)
    # TODO test book is not on the list
