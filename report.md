# The Pitt — Emergency Department Resilience Simulator: Report

*All results are from a synthetic, simplified model. They are simulation findings, not clinical predictions, and do not support real staffing or triage decisions.*

## 1. Problem
How do sudden demand surges, staff call-outs, and EHR downtime affect emergency-department flow, and which response strategies help most? The Pitt is used only as case-study inspiration; no real patient or hospital data are involved.

## 2. Method
A minute-step simulation of one 12-hour shift (`sim.py`). Arrivals are Poisson (21/hr, from `synthetic_patient_flow.csv`) with an ESI-like acuity mix. A priority queue feeds physicians, who evaluate each patient; the patient then occupies a treatment space. Usable capacity is min(spaces, nurses x 3 patients per nurse). An EHR outage multiplies evaluation and treatment time by 1.5 (1.2 with a downtime procedure). Strategies: surge capacity (+6 spaces), staff reallocation (+2 nurses), acuity prioritization, downtime procedure; surge capacity and reallocation start 30 minutes after the trigger. Every scenario is run 30 times with different seeds; tables report means with 95% confidence intervals (`scenario_results.csv`).

Baseline inputs: 30 spaces (12 monitored + 18 general), 9 nurses, 4 physicians (resource inventory and patient-flow file). Mass-casualty surge: 20 patients at minute 180. Call-outs: 2 nurses at minute 120. EHR outage: 90 minutes from minute 240.

## 3. Calibration
Evaluation-time scale (1.25) and patients per nurse (3.0) were chosen by grid search so baseline waits resemble the synthetic data. Result: model baseline mean wait 17 min and 90th percentile 49 min, versus 32 and 53 in the data. The 90th percentile is close; the mean is low, and the model's wait distribution is more skewed than the data's (many short waits, a long tail), which a queueing model cannot easily avoid. High-acuity waits in the model (about 2 min) are shorter than the data's ESI-2 median (about 12 min).

## 4. Results (mean of 30 runs)
| Scenario | Mean wait (min) | 90th pct (min) | Peak waiting | Still waiting at end | Treated |
|---|---|---|---|---|---|
| Normal operations | 17.1 | 49 | 18 | 8 | 222 |
| 2 nurse call-outs | 38.0 | 115 | 30 | 25 | 206 |
| Call-outs + 90-min EHR outage | 60.2 | 197 | 45 | 40 | 191 |
| Mass-casualty surge (+20) | 53.8 | 157 | 39 | 26 | 227 |
| Surge + call-outs + outage | 107.8 | 375 | 75 | 73 | 181 |
| Combined stress + all strategies | 69.8 | 213 | 47 | 36 | 217 |
| Combined + staff reallocation only | 81.2 | 257 | 53 | 44 | 208 |
| Combined + downtime procedure only | 95.9 | 321 | 65 | 62 | 191 |
| Combined + surge capacity only | 107.8 | 375 | 75 | 73 | 181 |

## 5. Answers to the project questions
- **Does adding staff reduce the wait?** Yes. Adding two nurses after the trigger cut mean wait under combined stress from 108 to 81 minutes.
- **How much does a surge increase the number waiting?** Peak queue rose from about 18 to about 39 patients (+20 patients at once).
- **Primary bottleneck?** Nurse-limited capacity, not physical space. Surge capacity alone changed nothing, because nurses, not spaces, set the cap in this model.
- **Effect of IT downtime on throughput?** A 90-minute outage added about 22 minutes to mean wait and reduced patients treated by about 15 (206 to 191) on top of the call-outs.
- **Best combination?** All strategies together gave the lowest waits (about 35% below no response), though still well above normal. Combinations of two strategies were not tested.
- **High-acuity patients:** with acuity priority, ESI 1-2 waits stayed under 4 minutes even under combined stress; the cost falls on lower-acuity patients.

## 6. Limitations
Synthetic data and assumptions; one shift; simplified provider, nurse and space logic; calibrated to a synthetic dataset, not a real ED; the nurse-bottleneck finding depends on the assumed 3 patients per nurse; the mean wait under-shoots the data; no clinical validation. Results should be re-tested with local data.

## 7. Recommendations (for further simulation work)
1. Test staff-reallocation triggers earlier than 30 minutes and in combination with the downtime procedure.
2. Track nurse-limited capacity, queue length, and time to surge recognition as early-warning measures in tabletop exercises.
3. Rehearse downtime documentation, since the outage cost throughput even with staff held constant.
4. Replace assumptions with local data and validate before any operational use.
