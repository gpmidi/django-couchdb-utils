from django.apps import AppConfig


class CouchDBUtilsSessionsConfig(AppConfig):
    name = 'django_couchdb_utils.sessions'
    verbose_name = "CouchDB Utils Auth"


app_label = 'couchsessions'
default_app_config = "django_couchdb_utils.sessions.CouchDBUtilsSessionsConfig"
