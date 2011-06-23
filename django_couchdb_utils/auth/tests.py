from django.contrib import auth as core_auth

from .models import User
from django_couchdb_utils.test.utils import DbTester


class AuthTests(DbTester):
    def test_user_registration(self):
        data = {
            'username': 'frank',
            'password': 'secret',
            'email': 'user@host.com',
        }
        user = User(**data)
        user.save()

        user = User.get_user(data['username'])
        self.assertIsNotNone(user)
        self.assertEqual(user.username, data['username'])

        user = User.get_user_by_email(data['email'])
        self.assertIsNotNone(user)
        self.assertEqual(user.username, data['username'])

    def test_username_uniqueness(self):
        data = {
            'username': 'frank',
            'password': 'secret',
        }
        user = User(**data)
        user.save()

        user2 = User(**data)
        self.assertExcMsg(Exception, 'This username is already in use.',
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
        self.assertExcMsg(Exception, 'This email address is already in use.',
                          user2.save)

    def test_user_authentication(self):
        authdata = {
            'username': 'mickey',
            'password': 'secret',
        }
        data = authdata.copy()
        data.update({
            'email': 'mickey@mice.com',
        })
        user = User(**data)
        user.set_password(data['password'])
        user.save()

        user = core_auth.authenticate(**authdata)

        self.assertIsNotNone(user)
