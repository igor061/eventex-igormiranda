from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):

    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_url_limits(self):
        for url in ('/xinscricao/', '/inscricaox/', '/xinscricao/'):
            self.assertEqual(404, self.client.get(url).status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"',1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """"Html must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context musthave subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        self.data = dict(name='Igor Miranda', cpf='12345678901', email='igor061@gmail.com', phone='61-99999-9999')
        self.resp = self.client.post('/inscricao/', self.data)

    def test_post(self):
        """Valid post should redirect ti /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribePostInvalid(TestCase):

    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid Post should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):

        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_sbuscription(self):
        self.assertFalse(Subscription.objects.exists())


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        self.data = dict(name='Igor Miranda', cpf='12345678901', email='igor061@gmail.com', phone='61-99999-9999')

        self.response = self.client.post('/inscricao/', self.data, follow=True)
        self.assertContains(self.response, 'Inscrição realizada com sucesso!')


