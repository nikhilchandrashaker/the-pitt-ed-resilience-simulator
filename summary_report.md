# Preliminary Results and Project Plan

## Purpose
This starter project explores how emergency-department demand, staffing, treatment-space availability, mass-casualty arrivals, and electronic-record downtime might interact in a simplified simulated system.

## Descriptive results from the generated data
- Simulated encounters: **500**
- Median triage-to-provider time: **32.0 minutes**
- 90th percentile triage-to-provider time: **53.0 minutes**
- Mean triage-to-provider time: **32.1 minutes**
- Median wait for rows flagged as mass-casualty-related: **50.5 minutes**
- Median wait for rows not flagged as mass-casualty-related: **31.0 minutes**
- Median wait for rows flagged during EHR downtime: **46.0 minutes**
- Median wait for rows outside EHR downtime: **30.0 minutes**

These figures describe the generated dataset only. They are not measurements of The Pitt, any real hospital, or real-world outcomes. The data generator intentionally includes operational stressors, so associations are partly built into the assumptions.

## Suggested research questions
1. How does the 90th percentile waiting time change as arrivals increase?
2. Which factors are associated with longer waits in this simulated environment?
3. How much does an added staffing pool reduce waiting times under a surge?
4. What continuity procedures should be tested during EHR downtime?
5. Which operational metrics help leaders recognize when surge capacity is being exceeded?

## Recommended methods
- Descriptive statistics and time-series plots for arrival volume and waits.
- Exploratory regression, with clear caveats about synthetic data.
- Discrete-event simulation for patient flow and resource constraints.
- Tabletop exercise evaluation using time-to-action and task-completion metrics.

## Interpretation guardrails
Do not interpret any synthetic association as evidence that the same effect size would occur in a real emergency department. The acuity labels are illustrative and not a clinical triage instrument. Actual plans should follow local emergency operations plans, validated clinical protocols, and qualified subject-matter review.
