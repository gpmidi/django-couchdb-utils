from django.test import TestCase


class TestHelper(TestCase):
    def assertExcMsg(self, exc, msg, callable, *args, **kw):
        '''
        Workaround for assertRaisesRegexp, which seems to be broken in stdlib. In
        theory the instructed use is:

        with self.assertRaisesRegexp(ValueError, 'literal'):
           int('XYZ')
       '''

        with self.assertRaises(exc) as cm:
            callable(*args, **kw)
        self.assertEqual(cm.exception.message, msg)
