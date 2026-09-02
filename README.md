# EDUKATE.ai learner progress summariser

A lightweight Python prototype for turning one employer cohort's learner progress payload into:

- an account-manager-ready employer summary;
- cohort-level metrics and learner statuses; and
- a JSON escalation payload for delivery teams.

## Run it

Requires Python 3.9 or later. The prototype uses only the standard library and
expects a local Ollama server when generating the AI summary.

```powershell
python learner_progress_summariser.py mock_payload.json
```

Install and start Ollama, then download the default model:

```powershell
ollama pull llama3.2
ollama serve
```

The model defaults to `llama3.2` and the API defaults to
`http://localhost:11434/api/generate`. Override them with `OLLAMA_MODEL` and
`OLLAMA_URL`. If Ollama is unavailable or returns invalid output, the report uses
the deterministic summary instead.

Pass the path to any compatible UTF-8 JSON payload as the required command-line argument. Call `load_payload(path)` and `generate_report(payload)` to use the summariser from another Python module.

## Prototype decisions

Status is deliberately deterministic and explainable:

- `at-risk`: two or more flags; attendance below 50%; off-the-job hours below 50% of target; or all three measures (attendance, assessment completion, and off-the-job hours) below 100%;
- `healthy`: no flags, attendance at least 85%, assessment completion at least 100%, and off-the-job hours at least 95% of target; and
- `borderline`: every remaining learner.

The rules are evaluated in that order, so at-risk takes priority over healthy when conditions overlap. Percentages are calculated from the corresponding scheduled, due, or target values; a zero denominator is treated as 100%.

The alert payload preserves machine-readable `reason_codes` and adds human-readable reasons and recommended actions. A production implementation should validate the payload schema, use stable learner IDs, keep an audit trail for generated text, and require a human review before employer delivery.
