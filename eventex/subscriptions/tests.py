from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscriptionsTest(TestCase):

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
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """"Html must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context musthave subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        self.data = dict(name='Igor Miranda', cpf='12345678901', email='igor061@gmail.com', phone='61-99999-9999')
        self.resp = self.client.post('/inscricao/', self.data)

        self.assertEqual(302, self.resp.status_code)

    def test_post(self):
        """Valid post should redirect ti /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'igor061@gmail.com']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        for chave, dado in self.data.items():
            self.assertIn(dado, email.body)

class SubscribeInvalidPost(TestCase):

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

class SubscritionSuccessMessage(TestCase):
    def test_message(self):
        self.data = dict(name='Igor Miranda', cpf='12345678901', email='igor061@gmail.com', phone='61-99999-9999')

        self.response = self.client.post('/inscricao/', self.data, follow=True)
        self.assertContains(self.response, 'Inscrição realizada com sucesso!')


