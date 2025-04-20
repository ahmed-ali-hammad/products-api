import json

from api.models import Item
from api.tasks import save_session_data
from api.tests.test_utils import sample_data
from django.test import Client, TestCase, override_settings


@override_settings(CELERY_ALWAYS_EAGER=True)
class ItemViewset(TestCase):
    def setUp(self):
        self.client = Client()
        save_session_data(json.loads(sample_data))

    def test_create(self):
        response = self.client.post(
            "/api/items/", data=sample_data, content_type="application/json"
        )

        self.assertEqual(response.data, {"detail": "Session data is being stored"})
        self.assertEqual(response.status_code, 200)

    def test_list_products(self):

        response = self.client.post("/api/items/list_products/")

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_remove_leading_zeros_from_code(self):

        self.assertEqual(Item.objects.all().first().code, "4311527127771")

    def test_parse_unicode_characters(self):

        self.assertEqual(
            Item.objects.all().first().description, "Walnüsse idS 30mm+ FR I 500g BT"
        )
