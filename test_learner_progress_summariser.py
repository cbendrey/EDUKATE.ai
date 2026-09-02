import unittest
from pathlib import Path

from learner_progress_summariser import generate_report, load_payload


PAYLOAD_PATH = Path(__file__).with_name("mock_payload.json")
mock_payload = load_payload(PAYLOAD_PATH)


class LearnerProgressSummariserTests(unittest.TestCase):
    def test_generates_expected_cohort_metrics(self):
        report = generate_report(mock_payload)

        self.assertEqual(report["cohort_metrics"]["learner_count"], 7)
        self.assertEqual(report["cohort_metrics"]["status_counts"], {
            "healthy": 2,
            "borderline": 3,
            "at-risk": 2,
        })
        self.assertEqual(report["cohort_metrics"]["attendance_percent"], 69.6)
        self.assertEqual(report["cohort_metrics"]["assessment_completion_percent"], 72.0)

    def test_escalates_only_flagged_or_at_risk_learners(self):
        report = generate_report(mock_payload)
        names = {alert["learner"] for alert in report["escalation_alerts"]}

        self.assertEqual(names, {"M. O'Brien", "K. Nowak", "T. Williams", "S. Adeyemi"})
        high_alerts = [
            alert for alert in report["escalation_alerts"] if alert["severity"] == "high"
        ]
        self.assertEqual({alert["learner"] for alert in high_alerts}, {"T. Williams", "S. Adeyemi"})


if __name__ == "__main__":
    unittest.main()
