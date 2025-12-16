from django.test import TestCase
from django.contrib.auth import get_user_model
from .management.commands.generate_monthly_bills import Command
from django.utils import timezone
from waste.models import WasteRecord
from payments.models import Payment


class BillingCommandTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='u1', password='pass')

    def test_generate_bill_no_pickups(self):
        cmd = Command()
        now = timezone.now()
        cmd.handle(year=now.year, month=now.month)
        p = Payment.objects.filter(user=self.user, month__year=now.year, month__month=now.month).first()
        self.assertIsNotNone(p)
        self.assertEqual(p.amount, 50)

    def test_generate_bill_with_extra_pickups(self):
        now = timezone.now()
        # create two waste records this month => 2 pickups -> extra 1
        WasteRecord.objects.create(user=self.user, waste_type='dry', entered_weight=1.0)
        WasteRecord.objects.create(user=self.user, waste_type='wet', entered_weight=2.0)
        cmd = Command()
        cmd.handle(year=now.year, month=now.month)
        p = Payment.objects.get(user=self.user, month__year=now.year, month__month=now.month)
        self.assertEqual(p.amount, 70)  # 50 + 20
