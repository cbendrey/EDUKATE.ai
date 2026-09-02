# Proposal: AI-Assisted Learner Progress Summariser

## Outcome

Give EDUKATE.ai delivery teams and account managers a fast, consistent view of learner progress, while giving employers clear visibility of achievements and the small number of learners needing support.

## Prototype scope

The prototype accepts a single employer cohort payload and calculates:

- attendance, assessment completion, and off-the-job learning percentages;
- explainable healthy, borderline, and at-risk statuses;
- an employer-facing summary paragraph; and
- structured escalation alerts with severity, reason codes, and suggested actions.

The current implementation uses AI for the summary generation but falls back to a deterministic implementation when there are issues with generating a response via AI. AI should improve phrasing and prioritisation only after the underlying metrics and rules are trusted.

## Suggested product flow

1. Ingest validated progress data at the end of a reporting period.
2. Calculate metrics and apply transparent risk rules.
3. Ask an AI model to draft a concise employer summary from the calculated facts.
4. Present the draft and escalation queue to a delivery user for review and edits.
5. Export or send the approved summary, with alerts routed to the responsible team.
6. Record source data, model version, prompt version, reviewer, and final message for auditability.

## Guardrails

- Never infer protected characteristics, diagnoses, or causes of disengagement.
- Treat flags as signals, not conclusions; show the underlying measures.
- Keep learner names and data access scoped to authorised employer users.
- Require human approval before external distribution.
- Avoid sending sensitive learner detail in alert titles or unencrypted channels.
- Make corrections and overrides visible in the audit history.

## Success measures

- Time for an account manager to prepare a monthly employer update.
- Percentage of summaries approved without factual correction.
- Delivery-team response time for high-severity alerts.
- Employer satisfaction with clarity and usefulness.
- False-positive and missed-intervention rates after agreed outcome review.

## Next increment

Add schema validation, stable learner IDs, persistence for report history, a review screen, configurable thresholds by programme, and tests for edge cases such as zero scheduled sessions and no assessments due. Then evaluate a model-assisted drafting step using redacted or synthetic data before production data is considered.
