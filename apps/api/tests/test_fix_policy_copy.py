import unittest


class RegressionTest(unittest.TestCase):
    def test_policy_mutation_does_not_change_catalog(self):
        from app.policies.catalog import get_policy
        policy = get_policy('support')
        original = get_policy('support')
        policy['weights']['privacy'] = 0
        policy['rules']['redact_pii'] = False
        self.assertEqual(get_policy('support'), original)


if __name__ == "__main__":
    unittest.main()
