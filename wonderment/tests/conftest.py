import django_webtest
import pytest

from wonderment.tests.client import TestClient


@pytest.fixture
def app(db, webtest):
    """Give a test access to a WebTest client for integration-testing views."""
    return TestClient()


@pytest.fixture
def no_csrf_app(app, webtest):
    """Give a test access to a CSRF-exempt WebTest client."""
    webtest._disable_csrf_checks()
    return app


@pytest.fixture
def xhr_app(no_csrf_app):
    """Give a test access to a CSRF-exempt XHR-by-default TestClient."""
    no_csrf_app.xhr_default = True
    return no_csrf_app


@pytest.fixture
def webtest(request):
    """
    Get an instance of a django-webtest TestCase subclass.

    We don't use TestCase classes, but we instantiate the django_webtest
    TestCase subclass in our web client fixtures to use its methods for
    patching/unpatching settings.

    """
    webtest = django_webtest.WebTest("__init__")

    webtest._patch_settings()
    request.addfinalizer(webtest._unpatch_settings)

    return webtest
