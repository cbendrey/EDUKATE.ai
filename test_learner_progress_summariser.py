import json
import unittest
from unittest.mock import patch
from pathlib import Path

from learner_progress_summariser import generate_report, load_payload, summary_generator


PAYLOAD_PATH = Path(__file__).with_name("Set1.json")
mock_payload = load_payload(PAYLOAD_PATH)


class LearnerProgressSummariserTests(unittest.TestCase):
    def test_generates_expected_cohort_metrics(self):
        report = generate_report(mock_payload, generate_summary=False)

        self.assertEqual(report["cohort_metrics"]["learner_count"], 7)
        self.assertEqual(report["cohort_metrics"]["status_counts"], {
            "healthy": 2,
            "borderline": 1,
            "at-risk": 4,
        })
        self.assertEqual(report["cohort_metrics"]["attendance_percent"], 71.4)
        self.assertEqual(report["cohort_metrics"]["assessment_completion_percent"], 72.0)

    def test_escalates_only_flagged_or_at_risk_learners(self):
        report = generate_report(mock_payload, generate_summary=False)
        names = {alert["learner"] for alert in report["escalation_alerts"]}

        self.assertEqual(names, {"R. Patel", "M. O'Brien", "K. Nowak", "T. Williams", "S. Adeyemi"})
        high_alerts = [
            alert for alert in report["escalation_alerts"] if alert["severity"] == "high"
        ]
        self.assertEqual({alert["learner"] for alert in high_alerts}, {"R. Patel", "M. O'Brien", "T. Williams", "S. Adeyemi"})

    @patch("learner_progress_summariser.summary_generator", return_value="AI employer summary")
    def test_uses_ollama_summary_generator(self, mocked_generator):
        report = generate_report(mock_payload)

        self.assertEqual(report["summary"], "AI employer summary")
        mocked_generator.assert_called_once()
        self.assertEqual(mocked_generator.call_args.args[0]["cohort_metrics"]["learner_count"], 7)

    @patch("learner_progress_summariser.summary_generator", side_effect=OSError("Ollama unavailable"))
    def test_falls_back_when_ollama_is_unavailable(self, mocked_generator):
        report = generate_report(mock_payload)
        fallback = generate_report(mock_payload, generate_summary=False)["summary"]

        self.assertEqual(report["summary"], fallback)
        mocked_generator.assert_called_once()

    @patch("learner_progress_summariser.urllib.request.urlopen")
    def test_ollama_prompt_contains_summary_guardrails_and_facts(self, mocked_urlopen):
        response = mocked_urlopen.return_value.__enter__.return_value
        response.read.return_value = json.dumps({"response": "A concise summary."}).encode()

        summary_generator({"attendance_percent": 71.4, "learner_count": 7})

        request = mocked_urlopen.call_args.args[0]
        request_payload = json.loads(request.data.decode())
        prompt = request_payload["prompt"].lower()
        self.assertIn("use only the supplied facts", prompt)
        self.assertIn("do not diagnose", prompt)
        self.assertIn("how many learners are healthy, borderline, and at-risk", prompt)
        self.assertIn("name every at-risk learner", prompt)
        self.assertIn("need more support", prompt)
        self.assertIn("number of distinct learners named as needing more support must exactly match", prompt)
        self.assertIn("at-risk means two or more flags", prompt)
        self.assertIn("healthy means no flags", prompt)
        self.assertIn("borderline means every remaining learner", prompt)
        self.assertIn("71.4", request_payload["prompt"])
        self.assertFalse(request_payload["stream"])


if __name__ == "__main__":
    unittest.main()
