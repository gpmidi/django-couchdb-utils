from couchdbkit.ext.django.schema import *
from couchdbkit.exceptions import ResourceNotFound

class Session(Document):
    session_key  = StringProperty()
    session_data = StringProperty()
    expire_date  = DateTimeProperty()

    class Meta:
        app_label = "django_couchdb_utils_sessions"

    @classmethod
    def get_session(cls, session_key):
        r = cls.view('%s/sessions_by_key' % cls._meta.app_label, key=session_key, include_docs=True)
        try:
            return r.first()
        except ResourceNotFound:
            return None


def cleanup_sessions(remove_all=False):
    r = Session.view('django_couchdb_utils/sessions_by_key', include_docs=True)
    for session in r.all():
        if remove_all or session.expire_date <= datetime.utcnow():
            session.delete()
