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
        sessions.cleanup_sessions(remove_all=options.get('remove_all'))
