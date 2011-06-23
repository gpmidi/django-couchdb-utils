from datetime import datetime, timedelta

from .models import Session, cleanup_sessions
from django_couchdb_utils.test.utils import DbTester


class SessionTests(DbTester):
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
