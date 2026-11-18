import unittest


class RegressionTest(unittest.TestCase):
    def test_unknown_audit_has_no_side_effects(self):
        from uuid import uuid4
        from app.schemas.review import ReviewRequest
        from app.services.demo_store import DemoStore
        store = DemoStore()
        request = ReviewRequest(audit_id=uuid4(), reviewer='Tester', decision='APPROVE')
        with self.assertRaisesRegex(ValueError, 'unknown evaluation'):
            store.add_review(request, 'BLOCK')
        self.assertEqual(store.reviews, [])
        self.assertEqual(store.analytics()['human_overrides'], 0)


if __name__ == "__main__":
    unittest.main()
