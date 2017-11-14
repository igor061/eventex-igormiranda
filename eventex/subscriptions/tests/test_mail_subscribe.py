

from django.core import mail
from django.test.testcases import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        self.data = dict(name='Igor Miranda', cpf='12345678901', email='igor061@gmail.com', phone='61-99999-9999')
        self.resp = self.client.post('/inscricao/', self.data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'igor061@gmail.com']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):

        for chave, dado in self.data.items():
            with self.subTest():
                self.assertIn(dado, self.email.body)