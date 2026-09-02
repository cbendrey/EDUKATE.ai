Given the following requirements

Hands-On Component (Python): Write a simple, working Python script (or small module) that takes a mock payload of learner progress data for one employer's cohort — sessions attended, assessments submitted, off-the-job hours logged, a couple of at-risk flags — and produces a summary an account manager could send to that employer, plus a formatted alert payload for anything that needs escalating. 

Generate a sample imput payload.

-------------------------

Please generate 5–8 learners with a deliberate mix: a couple healthy, a couple borderline, one or two clearly at-risk (missed sessions, behind on OTJ hours, overdue assessment).

-------------------------

Write a python script to meet the above requirements. Use the generated sample input payload as the input. 


--------------------------

Convert the input payload to .json and save to a separate file. Allow the path to the payload to be specified when the module is run. 

---------------------------

Change learner_status so that learners with less than 100% in all three categories (attendance, otj_completion and assessment_completion) also get flagged as at -risk

---------------------------

Add a comment to learner_status stating this new assumption and the others that have been made to determine the correct status. The decision making is the key part of the code and I want to explicitly comment on what it SHOULD be doing. 

---------------------------

Update the readme.md with the new learner status decisions

---------------------------

Please generate the human readable summary by making summary_generator call ollama to produce a concise employer-facing paragraph. The prompt should instruct the model to use only the supplied facts, avoid diagnosing or inferring causes, preserve all numbers exactly. The deterministic summary should remain as a reliable fallback.

---------------------------

Update the prompt so that the summary returns how many learners are in each status too. Also ensure that the names of the at-risk learners are flagged as needing more support.

---------------------------

Use the following rules in the prompt to make sure that Ollama is being consistent

at-risk: two or more flags; attendance below 50%; off-the-job hours below 50% of target; or all three measures (attendance, assessment completion, and off-the-job hours) below 100%;
healthy: no flags, attendance at least 85%, assessment completion at least 100%, and off-the-job hours at least 95% of target; and
borderline: every remaining learner.

---------------------------

Make sure this outputs a formatted Slack/email alert payload.

---------------------------

Create  launch configurations with different arguments for Slack, Email and JSON.