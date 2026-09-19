import unittest


class RegressionTest(unittest.TestCase):
    def test_invalid_weights(self):
        from copy import deepcopy
        from app.risk.engine import calculate_risk
        from app.policies.catalog import POLICIES
        for weights in ({}, {'privacy': 0}, {'privacy': -1}, {'privacy': float('nan')}, {'privacy': float('inf')}, {'privacy': True}, {'privacy': 1e308, 'bias': 1e308}):
            policy = deepcopy(POLICIES['support'])
            policy['weights'] = weights
            with self.assertRaises(ValueError):
                calculate_risk([], policy)
        self.assertEqual(calculate_risk([], POLICIES['support'])[0], 0)


if __name__ == "__main__":
    unittest.main()
