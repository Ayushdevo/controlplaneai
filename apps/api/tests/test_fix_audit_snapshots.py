import unittest


class RegressionTest(unittest.TestCase):
    def test_saved_and_fetched_objects_cannot_rewrite_audit(self):
        from app.schemas.evaluation import EvaluationResponse, Decision
        from app.services.demo_store import DemoStore
        record = EvaluationResponse(decision='BLOCK', risk_score=90, confidence=0.9, reasons=['original'], triggered_policies=[], detectors=[], evidence_coverage=0, latency_ms=1, detectors_run=[], application='support', recommended_action='Block', policy_name='test')
        store = DemoStore()
        returned = store.save_evaluation(record)
        record.reasons.append('mutation')
        returned.decision = Decision.ALLOW
        fetched = store.get_evaluation(record.audit_id)
        fetched.reasons.clear()
        store.list_incidents()[0].reasons.clear()
        self.assertEqual(store.get_evaluation(record.audit_id).reasons, ['original'])
        self.assertEqual(store.get_evaluation(record.audit_id).decision, Decision.BLOCK)


if __name__ == "__main__":
    unittest.main()
