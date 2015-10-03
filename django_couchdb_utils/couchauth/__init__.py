from django.apps import AppConfig


class CouchDBUtilsAuthConfig(AppConfig):
    name = 'django_couchdb_utils.couchauth'
    verbose_name = "CouchDB Utils Auth"


app_label = CouchDBUtilsAuthConfig.name
default_app_config = "django_couchdb_utils.couchauth.CouchDBUtilsAuthConfig"
