# The Pitt — ED Resilience Simulator (synthetic)
Run: `pip install -r requirements.txt && streamlit run app.py`
Replicated study: `python run_scenarios.py` (writes scenario_results.csv and charts).

## Model (sim.py)
Minute-step, one 12-hour shift. Poisson arrivals with an ESI mix; acuity-priority queue; physicians run evaluation, then a patient holds a treatment space.
Usable capacity = min(spaces, nurses x patients_per_nurse). EHR outage multiplies evaluation and treatment time (1.5x; 1.2x with downtime procedure).
Strategies: surge capacity (+6 spaces), staff reallocation (+2 nurses), both starting 30 min after trigger; acuity priority; downtime procedure.

## Calibration (see report)
Arrival rate (21/hr), staffing and space counts come from the project files. Evaluation-time scale (1.25) and patients-per-nurse (3.0) were tuned by grid search
so baseline waits land near the synthetic data (model mean ~17 min vs 32; 90th percentile ~49 vs 53). It does not match the data's tight wait distribution.

## Limitations
Synthetic and simplified; not validated against any real ED; no clinical or staffing recommendations. Findings are simulation results only.
