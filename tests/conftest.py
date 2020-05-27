import logging

import pytest

from booklist_app.app import create_app
from webtest import TestApp


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app()
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    testapp = TestApp(app)
    return testapp
