from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from locations.models import LocalBody, Ward
from waste.models import WasteRecord, Pickup
from workers.models import WorkerProfile
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone


class PickupWorkflowTests(TestCase):
    def setUp(self):
        self.lb = LocalBody.objects.create(name='TestLocal', body_type='panchayat')
        self.ward = Ward.objects.create(local_body=self.lb, name='W1', number=1)
        User = get_user_model()
        # regular user
        self.user = User.objects.create_user(username='u', password='pass')
        self.user.local_body = self.lb
        self.user.ward = self.ward
        self.user.save()
        # worker and profile
        self.worker_user = User.objects.create_user(username='worker', password='pass')
        self.worker_user.is_worker = True
        self.worker_user.save()
        self.worker = WorkerProfile.objects.create(user=self.worker_user, worker_id='W-1', local_body=self.lb, approved=True)
        self.worker.assigned_wards.add(self.ward)
        # staff user
        self.staff = User.objects.create_user(username='admin', password='pass', is_staff=True)
        self.client = Client()

    def test_pickup_created_on_waste_report(self):
        self.client.login(username='u', password='pass')
        resp = self.client.post(reverse('users:report_waste'), {'waste_type': 'dry', 'weight': '2.5'})
        self.assertEqual(resp.status_code, 302)
        wr = WasteRecord.objects.filter(user=self.user).first()
        self.assertIsNotNone(wr)
        self.assertTrue(hasattr(wr, 'pickup'))

    def test_admin_assigns_pickup(self):
        # create waste record
        wr = WasteRecord.objects.create(user=self.user, waste_type='dry', entered_weight=1.0)
        p = wr.pickup
        self.client.login(username='admin', password='pass')
        resp = self.client.post(reverse('adminpanel:assign_pickup', args=(p.id,)), {'worker': self.worker.id})
        self.assertRedirects(resp, reverse('adminpanel:pickups_list'))
        p.refresh_from_db()
        self.assertEqual(p.assigned_worker, self.worker)
        self.assertEqual(p.status, 'assigned')

    def test_assigned_worker_updates_pickup(self):
        wr = WasteRecord.objects.create(user=self.user, waste_type='dry', entered_weight=1.0)
        p = wr.pickup
        p.assigned_worker = self.worker
        p.status = 'assigned'
        p.save()
        self.client.login(username='worker', password='pass')
        proof = SimpleUploadedFile('proof.jpg', b'filecontent', content_type='image/jpeg')
        resp = self.client.post(reverse('workers:update_pickup', args=(p.id,)), {'status': 'completed', 'verified_weight': '0.9'}, follow=True, FILES={'worker_proof': proof})
        p.refresh_from_db()
        self.assertEqual(p.status, 'completed')
        self.assertIsNotNone(p.worker_proof_image)
        self.assertEqual(p.waste_record.verified_weight, 0.9)

    def test_non_assigned_worker_cannot_update(self):
        other_user = get_user_model().objects.create_user(username='other', password='pass')
        other_worker = WorkerProfile.objects.create(user=other_user, worker_id='W-2', local_body=self.lb, approved=True)
        wr = WasteRecord.objects.create(user=self.user, waste_type='wet', entered_weight=1.0)
        p = wr.pickup
        p.assigned_worker = self.worker
        p.save()
        self.client.login(username='other', password='pass')
        resp = self.client.post(reverse('workers:update_pickup', args=(p.id,)), {'status': 'completed'})
        self.assertRedirects(resp, reverse('workers:dashboard'))
        p.refresh_from_db()
        self.assertNotEqual(p.status, 'completed')

    def test_user_requests_reschedule(self):
        wr = WasteRecord.objects.create(user=self.user, waste_type='dry', entered_weight=1.0)
        p = wr.pickup
        self.client.login(username='u', password='pass')
        resp = self.client.post(reverse('users:request_reschedule', args=(p.id,)), {'scheduled_date': '2025-12-20'})
        self.assertRedirects(resp, reverse('users:dashboard'))
        p.refresh_from_db()
        self.assertEqual(p.status, 'requested')
        self.assertEqual(p.scheduled_date.isoformat(), '2025-12-20')
