from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from payments.models import Payment
from django.core import mail
from django.utils import timezone
from waste.models import WasteRecord


class PaymentsGatewayAndEmailTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('u1', password='p', email='u1@example.com')
        self.client = Client()

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_gateway_stub_marks_paid_and_sends_email(self):
        p = Payment.objects.create(user=self.user, amount=50, month=timezone.now().date(), invoice_number='INV-TEST')
        self.client.force_login(self.user)
        resp = self.client.post(f'/payments/gateway/{p.pk}/')
        self.assertEqual(resp.status_code, 302)
        p.refresh_from_db()
        self.assertTrue(p.paid)
        # ensure email sent
        self.assertGreaterEqual(len(mail.outbox), 1)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_generate_monthly_bills_sends_invoices(self):
        now = timezone.now()
        # no pickups
        call_command('generate_monthly_bills', year=now.year, month=now.month)
        # one email per user
        self.assertGreaterEqual(len(mail.outbox), 1)

    def test_pay_endpoint_marks_paid(self):
        p = Payment.objects.create(user=self.user, amount=50, month=timezone.now().date(), invoice_number='INV-TEST2')
        self.client.force_login(self.user)
        resp = self.client.post(f'/payments/pay/{p.pk}/')
        self.assertEqual(resp.status_code, 302)
        p.refresh_from_db()
        self.assertTrue(p.paid)
