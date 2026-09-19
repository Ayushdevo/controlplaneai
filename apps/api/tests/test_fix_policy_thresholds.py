import unittest


class RegressionTest(unittest.TestCase):
    def test_invalid_thresholds(self):
        from copy import deepcopy
        from app.risk.engine import calculate_risk
        from app.policies.catalog import POLICIES
        for thresholds in ({'modify':80,'review':40,'block':90}, {'modify':-1,'review':40,'block':90}, {'modify':20,'review':40,'block':101}, {'modify':True,'review':40,'block':90}, {}):
            policy = deepcopy(POLICIES['support'])
            policy['thresholds'] = thresholds
            with self.assertRaises(ValueError):
                calculate_risk([], policy)


if __name__ == "__main__":
    unittest.main()
