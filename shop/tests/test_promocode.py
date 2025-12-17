from django.test import TestCase
from shop.models import Product, PromoCode


class TestPromoCode(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(name="Toy", price=100)
        PromoCode.objects.create(code="TOYS10", discount_percent=10, is_active=True)

    def test_promocode_10(self):
        resp = self.client.get("/", {"code": "TOYS10"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["discount_percent"], 10)

    def test_bad_code(self):
        resp = self.client.get("/", {"code": "BAD"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["discount_percent"], 0)
        self.assertTrue(resp.context["promo_error"])
