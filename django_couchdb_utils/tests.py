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

from datetime import datetime, timedelta

from django.test import TestCase

from couchdbkit.ext.django.loading import get_db

from django_couchdb_utils.auth import User
from django_couchdb_utils.sessions import Session, cleanup_sessions


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

    def setUp(self):
        db = get_db('django_couchdb_utils')
        db.flush()


class AuthTests(TestHelper):
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


class SessionTests(TestHelper):
    def test_store_and_retrieve_session(self):

        # couchdbkit doesn't preserve microseconds
        timestamp = datetime.utcnow().replace(microsecond=0)

        data = {
            'session_key': 'dummy',
            'session_data': 'dummy',
            'expire_date': timestamp,
        }
        session = Session(**data)
        session.save()

        session = Session.get_session(data['session_key'])
        self.assertIsNotNone(session)

        for k, v in data.items():
            self.assertEqual(v, getattr(session, k))

    def test_cleanup_sessions(self):
        '''Created two sessions, one current, one outdated. Make sure the stale
        one is removed, the current is kept.'''
        data = {
            'session_key': 'dummy',
            'session_data': 'dummy',
            'expire_date': datetime.utcnow() - timedelta(minutes=1)
        }
        session = Session(**data)
        session.save()

        data2 = data.copy()
        data2.update({
            'session_key': 'dummy2',
            'expire_date': data['expire_date'] + timedelta(minutes=2)
        })
        session2 = Session(**data2)
        session2.save()

        cleanup_sessions()

        session = Session.get_session(data['session_key'])
        self.assertIsNone(session)

        session2 = Session.get_session(data2['session_key'])
        self.assertIsNotNone(session2)
