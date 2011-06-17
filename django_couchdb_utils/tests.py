"""
To run tests against couchdb you need to set TEST_RUNNER in settings.py:
TEST_RUNNER = 'couchdbkit.ext.django.testrunner.CouchDbKitTestSuiteRunner'

This will dispatch the right thing to the right place, but django's config
checks will still run, so make sure the DATABASES setting can pass scrutiny,
otherwise it errors out:

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME': 'throwaway.db',
    }
}

Then execute the test runner in the standard way:
$ python manage.py test django_couchdb_utils
"""

from django.test import TestCase

from couchdbkit.ext.django.loading import get_db

from django_couchdb_utils.auth import User


class AuthTests(TestCase):
    def setUp(self):
        db = get_db('labs')
        db.flush()

    def test_username_uniqueness(self):
        user = User(username='frank', password='secret')
        user.save()

        user2 = User(username='frank', password='secret')
        with self.assertRaisesRegexp(Exception, 'This username is already in use'):
            user2.save()

    def test_email_uniqueness(self):
        user = User(username='frank', password='secret', email='user@host.com')
        user.save()

        user2 = User(username='mark', password='secret', email='user@host.com')
        with self.assertRaisesRegexp(Exception, 'This email address is already in use'):
            user2.save()
