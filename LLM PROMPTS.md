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