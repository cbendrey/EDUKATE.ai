"""Prototype learner progress summary generator for EDUKATE.ai."""

from __future__ import annotations

import json
import argparse
from pathlib import Path
from typing import Any, Union


FLAG_LABELS = {
    "assessment_overdue": "assessment overdue",
    "attendance_declining": "attendance declining",
    "missed_last_2_sessions": "missed the last two sessions",
    "otj_hours_below_50pct": "off-the-job hours below 50% of target",
}


def load_payload(path: Union[str, Path]) -> dict[str, Any]:
    """Load one learner progress payload from a UTF-8 JSON file."""
    with Path(path).open(encoding="utf-8") as payload_file:
        payload = json.load(payload_file)
    if not isinstance(payload, dict):
        raise ValueError("The JSON root must be an object containing cohort data.")
    return payload


def percentage(value: float, total: float) -> float:
    return round(value / total * 100, 1) if total else 100.0


def learner_status(learner: dict[str, Any]) -> str:
    attendance = percentage(learner["sessions_attended"], learner["sessions_scheduled"])
    assessment_completion = percentage(
        learner["assessments_submitted"], learner["assessments_due"]
    )
    otj_completion = percentage(
        learner["off_the_job_hours_logged"], learner["off_the_job_hours_target"]
    )
    flags = learner["at_risk_flags"]

    if len(flags) >= 2 or attendance < 50 or otj_completion < 50:
        return "at-risk"
    if not flags and attendance >= 85 and assessment_completion >= 100 and otj_completion >= 95:
        return "healthy"
    if flags or attendance < 80 or assessment_completion < 100 or otj_completion < 100:
        return "borderline"
    return "borderline"


def build_alert(learner: dict[str, Any], status: str) -> dict[str, Any]:
    flag_codes = learner["at_risk_flags"]
    severity = "high" if status == "at-risk" else "medium"
    actions = []
    if "missed_last_2_sessions" in flag_codes:
        actions.append("Contact learner and employer to agree an attendance recovery plan")
    if "assessment_overdue" in flag_codes:
        actions.append("Confirm a submission date for overdue assessments")
    if "otj_hours_below_50pct" in flag_codes:
        actions.append("Review protected off-the-job learning time and schedule catch-up hours")
    if "attendance_declining" in flag_codes:
        actions.append("Monitor attendance trend and check for support needs")

    return {
        "learner": learner["name"],
        "severity": severity,
        "status": status,
        "reason_codes": flag_codes,
        "reasons": [FLAG_LABELS.get(code, code.replace("_", " ")) for code in flag_codes],
        "recommended_actions": actions,
    }


def generate_report(payload: dict[str, Any]) -> dict[str, Any]:
    learners = payload["learners"]
    statuses = {learner["name"]: learner_status(learner) for learner in learners}
    counts = {
        status: sum(current_status == status for current_status in statuses.values())
        for status in ("healthy", "borderline", "at-risk")
    }
    alerts = [
        build_alert(learner, statuses[learner["name"]])
        for learner in learners
        if statuses[learner["name"]] == "at-risk"
        or learner["at_risk_flags"]
    ]

    attendance = percentage(
        sum(learner["sessions_attended"] for learner in learners),
        sum(learner["sessions_scheduled"] for learner in learners),
    )
    assessment_completion = percentage(
        sum(learner["assessments_submitted"] for learner in learners),
        sum(learner["assessments_due"] for learner in learners),
    )
    otj_hours = sum(learner["off_the_job_hours_logged"] for learner in learners)
    otj_target = sum(learner["off_the_job_hours_target"] for learner in learners)

    summary = (
        f"During {payload['reporting_period']}, {payload['employer']} had "
        f"{len(learners)} learners in {payload['cohort']}. "
        f"Overall attendance was {attendance}%, assessment completion was "
        f"{assessment_completion}%, and the cohort logged {otj_hours:.1f} of "
        f"{otj_target:.1f} targeted off-the-job hours ({percentage(otj_hours, otj_target)}%). "
        f"{counts['healthy']} learners are healthy, {counts['borderline']} are borderline, "
        f"and {counts['at-risk']} are at risk. "
        f"Priority follow-up is recommended for {', '.join(alert['learner'] for alert in alerts if alert['severity'] == 'high') or 'no high-severity learners'}."
    )

    return {
        "employer": payload["employer"],
        "cohort": payload["cohort"],
        "reporting_period": payload["reporting_period"],
        "summary": summary,
        "cohort_metrics": {
            "learner_count": len(learners),
            "attendance_percent": attendance,
            "assessment_completion_percent": assessment_completion,
            "otj_hours_logged": round(otj_hours, 1),
            "otj_hours_target": round(otj_target, 1),
            "status_counts": counts,
        },
        "learner_statuses": statuses,
        "escalation_alerts": alerts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise learner progress from JSON.")
    parser.add_argument("payload_path", type=Path, help="Path to the learner progress JSON file")
    args = parser.parse_args()

    try:
        report = generate_report(load_payload(args.payload_path))
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as error:
        parser.error(f"could not process {args.payload_path}: {error}")

    print("EMPLOYER SUMMARY")
    print(report["summary"])
    print("\nESCALATION PAYLOAD")
    print(json.dumps(report["escalation_alerts"], indent=2))


if __name__ == "__main__":
    main()
