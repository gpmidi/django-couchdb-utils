from datetime import datetime
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.contrib.sessions.backends.base import SessionBase, CreateError
from couchdbkit.ext.django.schema import *


class SessionStore(SessionBase):

    def create(self):
        while True:
            self.session_key = self._get_new_session_key()
            self.modified = True
            self._session_cache = {}
            try:
                self.save(must_create=True)
            except CreateError:
                continue
            return None

    def load(self):
        session = Session.get_session(self.session_key)
        if not session:
            self.create()
            return {}
        try:
            return self.decode(session.session_data)
        except SuspiciousOperation:
            return {}

    def save(self, must_create=False):
        session = Session.get_session(self.session_key)
        if must_create and session:
            raise CreateError
        if must_create:
            session = Session()
            session.session_key = self.session_key
            session.session_data = self.encode(self._get_session(no_load=must_create))
            session.expire_date = self.get_expiry_date()
        else:
            if not session:
                return None
            session.session_data = self.encode(self._get_session(no_load=must_create))
            session.expire_date = self.get_expiry_date()
        session.save()

    def exists(self, session_key):
        session = Session.get_session(session_key)
        if session is None:
            return False
        return True

    def delete(self, session_key=None):
        if not session_key:
            if not self._session_key:
                return None
            session_key = self._session_key
        session = Session.get_session(session_key)
        if not session:
            return None
        session.delete()


def cleanup_sessions(remove_all=False):
    r = Session.view('django_couchdb_utils/sessions_by_key', include_docs=True)
    for session in r.all():
        if remove_all or session.expire_date <= datetime.utcnow():
            session.delete()
