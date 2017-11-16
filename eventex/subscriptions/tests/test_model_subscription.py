from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Igor Miranda',
            cpf='12345678901',
            email='igor061@gmail.com',
            phone='61-99999-9999',
        )

        self.obj.save()

    def test_creat(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an outo created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual(self.obj.name, str(self.obj))