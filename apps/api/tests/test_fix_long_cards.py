import unittest


class RegressionTest(unittest.TestCase):
    def test_long_card_is_fully_redacted(self):
        from app.detectors.pii import detect_pii
        for number in ('1234567890123456789', '1234 5678 9012 3456 789'):
            result, redacted = detect_pii('Card: ' + number + '.')
            self.assertTrue(result.detected)
            self.assertEqual(redacted, 'Card: [CREDIT_CARD_REDACTED].')
            self.assertEqual(result.metadata['entities'][0]['type'], 'CREDIT_CARD')


if __name__ == "__main__":
    unittest.main()
