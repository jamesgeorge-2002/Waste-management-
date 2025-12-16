from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from locations.models import LocalBody, Ward
from workers.models import WorkerProfile
from waste.models import WasteRecord, Pickup
from django.core.files.uploadedfile import SimpleUploadedFile


class WorkerPickupUpdateTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('u1', password='p')
        self.worker_user = User.objects.create_user('w1', password='p')
        self.worker_user.is_worker = True
        self.worker_user.save()
        self.lb = LocalBody.objects.create(name='LB', body_type='panchayat')
        self.ward = Ward.objects.create(local_body=self.lb, name='W', number=1)
        self.worker = WorkerProfile.objects.create(user=self.worker_user, worker_id='W001', local_body=self.lb, approved=True)
        self.worker.assigned_wards.add(self.ward)
        self.waste = WasteRecord.objects.create(user=self.user, waste_type='dry', entered_weight=3.0)
        # assign pickup to worker
        self.pickup = self.waste.pickup
        self.pickup.assigned_worker = self.worker
        self.pickup.save()
        self.client = Client()

    def test_worker_verifies_and_completes(self):
        self.client.force_login(self.worker_user)
        file_data = SimpleUploadedFile('proof.jpg', b'fake-image-bytes', content_type='image/jpeg')
        resp = self.client.post(f'/workers/pickup/{self.pickup.id}/update/', {'status': 'completed', 'verified_weight': '2.5', 'worker_proof': file_data})
        self.assertEqual(resp.status_code, 302)
        self.waste.refresh_from_db()
        self.pickup.refresh_from_db()
        self.assertEqual(self.waste.verified_weight, 2.5)
        self.assertEqual(self.pickup.status, 'completed')
        self.assertTrue(bool(self.pickup.worker_proof_image))
