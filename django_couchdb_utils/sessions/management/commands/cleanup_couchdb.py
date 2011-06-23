from django.core.management.base import BaseCommand
from optparse import make_option
from django_couchdb_utils import sessions

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--remove-all',
                    action='store_true',
                    dest='remove_all',
                    default=False,
                    help='Remove all sessions, not just stale'),
    )

    def handle(self, *args, **options):
        cleanup_sessions(remove_all=options.get('remove_all'))


def cleanup_sessions(remove_all=False):
    r = Session.view('django_couchdb_utils/sessions_by_key', include_docs=True)
    for session in r.all():
        if remove_all or session.expire_date <= datetime.utcnow():
            session.delete()
