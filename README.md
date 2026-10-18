# The Pitt — Emergency Management Project Starter Pack

## Project question
How do sudden demand surges, staffing shortfalls, constrained treatment spaces, and information-system downtime affect simulated emergency-department flow and operational resilience?

## Files
- `synthetic_patient_flow.csv`: 500 simulated encounter rows across two simulated 12-hour shifts.
- `episode_theme_catalog.csv`: a small catalog of operational themes coded from publicly available episode summaries. It is not a complete episode transcript or exhaustive scene log.
- `tabletop_scenarios.csv`: six tabletop exercises with triggers, response options, and evaluation metrics.
- `resource_inventory.csv`: illustrative resource/capacity assumptions to replace with local planning data if available.
- `hourly_metrics.csv`: aggregated descriptive metrics by simulated shift and hour.
- `analysis.py`: reproducible starter analysis and charts.
- `summary_report.md`: short interpretation and limitations.
- `the_pitt_project_workbook.xlsx`: multi-sheet workbook containing the tables and a summary sheet.

## Important data status
All encounter-level records, times, staffing numbers, waits, treatment durations, capacity values, dispositions, and scenario quantities are synthetic and generated for this project. They are not from the show, a hospital, or actual patient records. Episode themes are high-level summaries based on public episode-guide descriptions, not verbatim dialogue or a complete scene-by-scene dataset.

## Acuity note
`triage_acuity_esi` uses ESI-like labels for a familiar educational vocabulary. The generated labels are not clinical triage assessments and should not be used for patient care, operational staffing decisions, or validation of clinical policy.

## Suggested analysis
1. Compare arrivals and median / 90th percentile waiting time by hour.
2. Compare wait time across acuity groups and flag whether high-acuity waits behave as intended in the synthetic generator.
3. Fit an exploratory regression for wait time using acuity, available spaces, nurse count, downtime, and surge flag.
4. Run scenario perturbations (e.g. +20% arrivals, -2 nurses, 90-minute downtime) and compare outcomes.
5. Convert the scenarios into a tabletop exercise with an observer scorecard.

## Limitations
- Synthetic assumptions are illustrative, not calibrated to any real ED.
- The dataset is designed for analytics practice, not clinical inference.
- Episode summaries are secondary sources and may omit context. Verify details against episodes if producing episode-level claims.
- Do not use the data to recommend actual staffing ratios, clinical thresholds, or triage protocols.
