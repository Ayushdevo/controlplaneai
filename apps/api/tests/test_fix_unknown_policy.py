import unittest


class RegressionTest(unittest.TestCase):
    def test_typo_does_not_select_support_policy(self):
        from app.policies.catalog import get_policy
        with self.assertRaisesRegex(ValueError, 'Unknown application'):
            get_policy('finanical')
        self.assertEqual(get_policy('financial')['name'], 'Financial Decision Assistant')


if __name__ == "__main__":
    unittest.main()
