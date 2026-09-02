# EDUKATE.ai learner progress summariser

A lightweight Python prototype for turning one employer cohort's learner progress payload into:

- an account-manager-ready employer summary;
- cohort-level metrics and learner statuses; and
- a JSON escalation payload for delivery teams.

## Run it

Requires Python 3.9 or later. The prototype uses only the standard library.

```powershell
python learner_progress_summariser.py mock_payload.json
```

Pass the path to any compatible UTF-8 JSON payload as the required command-line argument. Call `load_payload(path)` and `generate_report(payload)` to use the summariser from another Python module.

## Prototype decisions

Status is deliberately deterministic and explainable:

- `healthy`: no flags, attendance at least 85%, assessment completion at 100%, and off-the-job hours at least 95% of target;
- `borderline`: a flag exists or one measure is below target; and
- `at-risk`: two or more flags, attendance below 50%, or off-the-job hours below 50% of target.

The alert payload preserves machine-readable `reason_codes` and adds human-readable reasons and recommended actions. A production implementation should validate the payload schema, use stable learner IDs, keep an audit trail for generated text, and require a human review before employer delivery.
