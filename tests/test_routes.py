import pytest
from app_files.db_interface import DBInterface


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
BOOK2 = {
    "title": "Grapes of Wrath",
    "author": "Fiona O'Connell",
    "isbn": "123-4-56-123456-0",
    "pub_date": "1960-01-02",
}


@pytest.fixture
def setup():
    DBInterface.clear_database()
    DBInterface.setup_database()
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
    assert res.json["data"] == ["roger@gmail.com", "Roger", "Blankman"]


def test_add_user_with_user_already_existing(setup, testapp):
    # try to add the same user twice
    testapp.post_json("/add_user", USER1, status=200)
    res = testapp.post_json("/add_user", USER1, status=409)
    assert res.json["status"] == "User already exists"


def test_add_book(setup, testapp):
    res = testapp.post_json("/add_book", BOOK1, status=200)
    assert res.json["status"] == "Book added"

    params = "?isbn=978-3-16-148410-0"
    res = testapp.get(f"/get_book{params}", status=200)
    assert res.json["data"] == [
        "978-3-16-148410-0",
        "Tiamat's Wrath",
        "James S. Corey",
        "2020-03-24",
    ]


def test_add_book_with_book_already_existing(setup, testapp):
    # try to add the same book twice
    testapp.post_json("/add_book", BOOK1, status=200)
    res = testapp.post_json("/add_book", BOOK1, status=409)
    assert res.json["status"] == "Book already exists"


def test_get_user(setup, testapp):
    # create a user to be fetched
    testapp.post_json("/add_user", USER1, status=200)

    params = "?email=roger@gmail.com"
    res = testapp.get(f"/get_user{params}", status=200)
    assert res.json["status"] == "User returned"
    assert res.json["data"] == ["roger@gmail.com", "Roger", "Blankman"]


def test_get_book(setup, testapp):
    # create a book to be fetched
    testapp.post_json("/add_book", BOOK1, status=200)

    params = "?isbn=978-3-16-148410-0"
    res = testapp.get(f"/get_book{params}", status=200)
    assert res.json["status"] == "Book returned"
    assert res.json["data"] == [
        "978-3-16-148410-0",
        "Tiamat's Wrath",
        "James S. Corey",
        "2020-03-24",
    ]


def test_get_list(setup, testapp):
    # create a list to be fetched
    testapp.post_json("/add_user", USER1, status=200)
    testapp.post_json("/add_book", BOOK1, status=200)
    testapp.post_json("/add_book", BOOK2, status=200)
    testapp.post_json(
        "/add_book_to_list", {"email": USER1["email"], "isbn": BOOK1["isbn"]}
    )
    testapp.post_json(
        "/add_book_to_list", {"email": USER1["email"], "isbn": BOOK2["isbn"]}
    )

    params = "?email=roger@gmail.com"
    res = testapp.get(f"/get_list{params}", status=200)
    assert res.json["status"] == "List returned"
    assert res.json["data"] == [
        [USER1["email"], BOOK2["isbn"]],
        [USER1["email"], BOOK1["isbn"]],
    ]


def test_update_user(setup, testapp):
    # create a user to be updated
    testapp.post_json("/add_user", USER1, status=200)

    res = testapp.post_json(
        "/update_user", {"email": "roger@gmail.com", "first_name": "Bob"}, status=200
    )

    assert res.json["status"] == "User updated"

    params = "?email=roger@gmail.com"
    res = testapp.get(f"/get_user{params}", status=200)
    assert res.json["data"] == [USER1["email"], "Bob", "Blankman"]


def test_update_book(setup, testapp):
    # create a book to be updated
    testapp.post_json("/add_book", BOOK1, status=200)

    res = testapp.post_json(
        "/update_book",
        {"isbn": "978-3-16-148410-0", "author": "Paul Patrick"},
        status=200,
    )
    assert res.json["status"] == "Book updated"

    params = "?isbn=978-3-16-148410-0"
    res = testapp.get(f"/get_book{params}", status=200)
    assert res.json["data"] == [
        BOOK1["isbn"],
        BOOK1["title"],
        "Paul Patrick",
        BOOK1["pub_date"],
    ]


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
    assert res.json["data"] == [[USER1["email"], BOOK1["isbn"]]]


def test_remove_book_from_list(setup, testapp):
    # create a list with two books on it
    testapp.post_json("/add_book", BOOK1, status=200)
    testapp.post_json("/add_book", BOOK2, status=200)
    testapp.post_json("/add_user", USER1, status=200)
    testapp.post_json(
        "/add_book_to_list",
        {"email": USER1["email"], "isbn": BOOK1["isbn"]},
        status=200,
    )
    testapp.post_json(
        "/add_book_to_list",
        {"email": USER1["email"], "isbn": BOOK2["isbn"]},
        status=200,
    )

    # remove one of the books
    res = testapp.post_json(
        "/remove_book_from_list",
        {"email": USER1["email"], "isbn": BOOK1["isbn"]},
        status=200,
    )
    assert res.json["status"] == "Book removed from list"

    # confirm book1 was removed, leaving only book2
    res = testapp.get("/get_list", {"email": USER1["email"]}, status=200)
    assert res.json["data"] == [[USER1["email"], BOOK2["isbn"]]]


def test_remove_book_that_is_not_on_wishlist(setup, testapp):
    res = testapp.post_json(
        "/remove_book_from_list", {"email": "roger@blank.com", "isbn": "92"}, status=404
    )
    assert res.json["status"] == "Book not found on wishlist"


def test_delete_user(setup, testapp):
    # create a user to be deleted
    testapp.post_json("/add_user", USER1, status=200)

    res = testapp.post_json("/delete_user", {"email": "roger@gmail.com"}, status=200)

    assert res.json["status"] == "User deleted"

    # try to fetch user
    params = "?email=roger@gmail.com"
    res = testapp.get(f"/get_user{params}", status=404)
    assert res.json["status"] == "User not found"


def test_delete_user_and_wishlist(setup, testapp):
    # create a list
    testapp.post_json("/add_book", BOOK1, status=200)
    testapp.post_json("/add_user", USER1, status=200)
    testapp.post_json(
        "/add_book_to_list",
        {"email": USER1["email"], "isbn": BOOK1["isbn"]},
        status=200,
    )

    # delete the user
    testapp.post_json("/delete_user", {"email": USER1["email"]}, status=200)

    # try to fetch list
    params = "?email=roger@gmail.com"
    res = testapp.get(f"/get_list{params}", status=404)
    assert res.json["status"] == "No wishlist found for User"


def test_delete_book(setup, testapp):
    # create a book to be deleted
    testapp.post_json("/add_book", BOOK1, status=200)

    res = testapp.post_json("/delete_book", {"isbn": "978-3-16-148410-0"}, status=200)

    assert res.json["status"] == "Book deleted"

    params = "?isbn=978-3-16-148410-0"
    res = testapp.get(f"/get_book{params}", status=404)
    assert res.json["status"] == "Book not found"
