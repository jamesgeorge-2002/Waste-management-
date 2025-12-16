from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from locations.models import LocalBody, Ward
from workers.models import WorkerProfile
from waste.models import WasteRecord, Pickup


class AdminPickupAssignTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.staff = User.objects.create_user('staff', password='s', is_staff=True)
        self.user = User.objects.create_user('u1', password='p')
        self.lb = LocalBody.objects.create(name='Test LB', body_type='panchayat')
        self.ward = Ward.objects.create(local_body=self.lb, name='Ward1', number=1)
        self.worker_user = User.objects.create_user('w1', password='p')
        self.worker_user.is_worker = True
        self.worker_user.save()
        self.worker = WorkerProfile.objects.create(user=self.worker_user, worker_id='W001', local_body=self.lb, approved=True)
        self.worker.assigned_wards.add(self.ward)
        # create waste and pickup
        self.waste = WasteRecord.objects.create(user=self.user, waste_type='dry', entered_weight=2.0)
        self.pickup = self.waste.pickup
        self.client = Client()

    def test_assign_pickup(self):
        self.client.force_login(self.staff)
        resp = self.client.post(f'/adminpanel/pickups/{self.pickup.id}/assign/', {'worker': self.worker.id})
        self.assertEqual(resp.status_code, 302)
        self.pickup.refresh_from_db()
        self.assertEqual(self.pickup.assigned_worker, self.worker)
        self.assertEqual(self.pickup.status, 'assigned')
