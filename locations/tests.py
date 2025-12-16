from django.test import TestCase, Client
from .models import LocalBody, Ward


class APITests(TestCase):
    def setUp(self):
        self.lb = LocalBody.objects.create(name='Test Panchayat', body_type='panchayat')
        Ward.objects.create(local_body=self.lb, name='North', number=1)
        Ward.objects.create(local_body=self.lb, name='South', number=2)
        self.client = Client()

    def test_wards_api(self):
        resp = self.client.get(f'/locations/api/wards/?local_body={self.lb.id}')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('wards', data)
        self.assertEqual(len(data['wards']), 2)
