# HadiProjects

Projects I worked on during my Computer Science degree at Beirut Arab University.

## SAWTAK (Senior Project)

Sawtak (صوتك, "Your Voice") is a Lebanese social platform meant to make online
debate less toxic. Instead of a normal feed, users respond to posts with
Agree / Disagree, and the platform uses AI to classify posts by topic and opinion.
It has two main features: an "Echo Chamber Breaker" that recommends posts with
views different from your own, and a news verification tool that checks claims
against trusted sources and gives an evidence score from 0 to 5.
Privacy was a core rule: the platform never stores or guesses a user's religion,
sect, or political affiliation.

This first phase covered requirements, a survey of 88 Lebanese users, feasibility
study, UI prototypes, and full system design. Team project with 4 other students.
Planned stack: React, Node.js, Supabase / PostgreSQL.

Report: SAWTAK senior project .docx

## Phishing Email Detection (Machine Learning)

Built a classifier that detects phishing emails targeting bank customers.
I created a dataset of 2,600 emails, cleaned the text, and used TF-IDF plus
extra features like number of links, urgent wording, and spelling mistakes.
I compared Naive Bayes with Logistic Regression, Linear SVM, and Decision Tree.
Naive Bayes did best with 97.1% accuracy and 0.97 ROC AUC, and was also the
fastest to train.

Built with Python and scikit-learn.

Code, report and slides: HadiMuselmani ML PROJECT.zip

## Zero-Trust Security on Azure (Cloud Project)

Set up a zero-trust identity and access system on Microsoft Azure using Entra ID.
I created a tenant with multiple users and roles, gave each one only the access
they needed (RBAC), added Conditional Access rules for MFA and location limits,
used a Managed Identity so an Azure Function could run without stored passwords,
and wrote KQL queries in Log Analytics to spot suspicious sign-ins.

Report: HadiMuselmani cloud project.docx

## CPU Scheduling and Banker's Algorithm (Operating Systems)

Simulated FCFS CPU scheduling with 12 processes in an OS simulator, recorded
waiting and turnaround times, and drew the Gantt chart (average waiting time
was 54.25). In the second part I used the Banker's Algorithm on 4 processes and
3 resource types to calculate the Need matrix and check if the system was in a
safe state.

Report: Os Project Had Muselmani.docx

## Contact

Portfolio: https://hadimuselmani.github.io
Email: hmuselmani86@gmail.com
