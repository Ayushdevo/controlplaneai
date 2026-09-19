import unittest


class RegressionTest(unittest.TestCase):
    def test_conversation_id_validation(self):
        from pydantic import ValidationError
        from app.schemas.evaluation import EvaluationRequest
        for value in ('', '   ', 'x' * 129):
            with self.assertRaises(ValidationError):
                EvaluationRequest(input='hello', conversation_id=value)
        self.assertIsNone(EvaluationRequest(input='hello').conversation_id)
        self.assertEqual(EvaluationRequest(input='hello', conversation_id='x' * 128).conversation_id, 'x' * 128)


if __name__ == "__main__":
    unittest.main()
