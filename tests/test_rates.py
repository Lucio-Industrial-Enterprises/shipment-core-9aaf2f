import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_invalid_weight(self):
        for service in ("standard", "express"):
            for weight in (0, -1):
                with self.subTest(service=service, weight=weight):
                    with self.assertRaisesRegex(ValueError, "weight must be positive"):
                        shipping_quote(weight, "local", service=service)

    def test_explicit_standard_matches_default(self):
        for zone in ("local", "regional"):
            for weight in (0.1, 2, 3.141):
                with self.subTest(zone=zone, weight=weight):
                    self.assertEqual(
                        shipping_quote(weight, zone, service="standard"),
                        shipping_quote(weight, zone),
                    )

    def test_express_rates(self):
        self.assertEqual(shipping_quote(2, "local", service="express"), 15.0)
        self.assertEqual(shipping_quote(2, "regional", "express"), 18.0)

    def test_fractional_weights_are_rounded(self):
        for zone, base in (("local", 5), ("regional", 8)):
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(3.141, zone), base + 4.71)
                self.assertEqual(shipping_quote(3.141, zone, "express"), base + 11.71)

    def test_invalid_zone(self):
        for service in ("standard", "express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown zone"):
                    shipping_quote(2, "unknown", service=service)

    def test_invalid_service(self):
        with self.assertRaisesRegex(ValueError, "unknown service"):
            shipping_quote(2, "local", service="overnight")
