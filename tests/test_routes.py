import pytest
import sqlite3
from app_files.config import constants


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
    conn = sqlite3.connect(constants.DB_NAME_TEST)
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS Users""")
    cur.execute("""DROP TABLE IF EXISTS Books""")
    cur.execute("""DROP TABLE IF EXISTS Lists""")
    conn.commit()

    setup = {"conn": conn}
    yield setup
    conn.close()


def test_index(setup, testapp):
    res = testapp.get("/")
    assert res.status_code == 200
    assert res.json["status"] == "OK"

    res = testapp.get("/index")
    assert res.status_code == 200
    assert res.json["status"] == "OK"


def test_add_user(setup, testapp):
    res = testapp.post("/add_user", USER1, status=200)
    assert res.json["status"] == "User added"


def test_get_list(setup, testapp):
    # create a list to be fetched
    testapp.post("/add_user", USER1, status=200)
    testapp.post("/add_book", BOOK1, status=200)
    testapp.post("/add_book_to_list", {"email": "roger@gmail.com", "isbn": ""})

    params = "?email=roger@gmail.com"
    res = testapp.get(f"/get_list{params}", status=200)
    assert res.json["status"] == "List returned"


def test_update_user(setup, testapp):
    # create a user to be updated
    testapp.post("/add_user", USER1, status=200)

    res = testapp.post("/update_user", {"email": "roger@gmail.com", "first_name": "Bob"}, status=200)

    assert res.json["status"] == "User updated"


def test_delete_user(setup, testapp):
    # create a user to be deleted
    testapp.post("/add_user", USER1, status=200)

    res = testapp.post("/delete_user", {"email": "roger@gmailcom"}, status=200)

    assert res.json["status"] == "User deleted"


def test_add_book(setup, testapp):
    res = testapp.post("/add_book", BOOK1, status=200)
    assert res.json["status"] == "Book added"


def test_delete_book(setup, testapp):
    # create a book to be deleted
    testapp.post("/add_book", BOOK1, status=200)

    res = testapp.post("/delete_book", {"isbn": "978-3-16-148410-0"}, status=200)

    assert res.json["status"] == "Book deleted"


def test_update_book(setup, testapp):
    # create a book to be updated
    testapp.post("/add_book", BOOK1, status=200)

    res = testapp.post("/update_book", {"isbn": "978-3-16-148410-0", "author": "Paul Patrick"}, status=200)
    assert res.json["status"] == "Book updated"


def test_add_book_to_list(setup, testapp):
    # create a book and a user
    testapp.post("/add_book", BOOK1, status=200)
    testapp.post("/add_user", USER1, status=200)

    res = testapp.post("/add_book_to_list", {"email": "roger@gmail.com", "isbn": "978-3-16-148410-0"}, status=200)
    assert res.json["status"] == "Book added to list"


def test_remove_book(setup, testapp):
    # create a list with a book to be removed
    testapp.post("/add_book", BOOK1, status=200)
    testapp.post("/add_user", USER1, status=200)
    testapp.post("/add_book_to_list", {"email": USER1["email"], "isbn": BOOK1["isbn"]}, status=200)

    res = testapp.post("/remove_book_from_list", {"email": USER1["email"], "isbn": BOOK1["isbn"]}, status=200)
    assert res.json["status"] == "Book removed from list"
