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


class TestHelper(TestCase):
    def exc_msg_is(self, exc, msg, callable, *args, **kw):
        '''
        Workaround for assertRaisesRegexp, which seems to be broken in stdilb. In
        theory the instructed use is:

        with self.assertRaisesRegexp(ValueError, 'literal'):
           int('XYZ')
       '''

        with self.assertRaises(exc) as cm:
            callable(*args, **kw)
        self.assertEqual(cm.exception.message, msg)


class AuthTests(TestHelper):
    def setUp(self):
        db = get_db('django_couchdb_utils')
        db.flush()

    def test_username_uniqueness(self):
        data = {
            'username': 'frank',
            'password': 'secret',
        }
        user = User(**data)
        user.save()

        user2 = User(**data)
        self.exc_msg_is(Exception, 'This username is already in use',
                        user2.save)

    def test_email_uniqueness(self):
        data = {
            'username': 'frank',
            'password': 'secret',
            'email': 'user@host.com',
        }
        user = User(**data)
        user.save()

        data.update({
            'username': 'mark',
        })
        user2 = User(**data)
        self.exc_msg_is(Exception, 'This email address is already in use',
                        user2.save)
