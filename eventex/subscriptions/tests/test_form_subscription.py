from django.test.testcases import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):

    def setUp(self):
        self.form = SubscriptionForm()
#        form = self.response.context['form']

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        expect = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expect, list(self.form.fields))
