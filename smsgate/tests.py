import json

from django.utils import unittest
from django.test.client import Client
from smsgate.models import Partner, QueueItem

class SendTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

        p = Partner(name='test partner')
        p.save()

        self.partner_id = p.id


    def get_json(self, to, args_dict):
        str_response = self.client.post(to, args_dict)
        return json.loads(str_response.content)


    def test_ok(self):
        """
        Valid partner - valid status.
        """
        message = 'Some message for you man'

        resp = self.get_json('/sms/send/', {'partner_id': self.partner_id, 'message': message})
        self.assertEqual(resp['status'], 0)
        queue_id = resp['id']
        qi = QueueItem.objects.get(pk=queue_id)

        self.assertEqual(self.partner_id, qi.partner_id)
        self.assertEqual(message, qi.message)


    def test_bad_partner(self):
        """
        Invalid partner id should cause status 1.
        """
        resp = self.get_json('/sms/send/', {'partner_id': 9000, 'message': 'msg'})
        self.assertEqual(resp['status'], 1)
