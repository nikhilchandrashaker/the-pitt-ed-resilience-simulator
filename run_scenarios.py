"""Replicated scenario study -> scenario_results.csv, chart_wait.png, chart_queue.png"""
import pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sim import *
STRESS = dict(surge_patients=20, nurse_callouts=2, downtime_min=90)
S = dict(SCENARIOS)
S["Combined stress + all strategies"] = Params(**STRESS, surge_capacity=True, reallocate_staff=True, downtime_procedure=True)
S["Combined stress + surge capacity only"] = Params(**STRESS, surge_capacity=True)
S["Combined stress + staff reallocation only"] = Params(**STRESS, reallocate_staff=True)
S["Combined stress + downtime procedure only"] = Params(**STRESS, downtime_procedure=True)
rows = []
for k, v in S.items():
    r = summarize(run_many(v, 30))
    rows.append({"scenario": k, **{m: r.loc[m, "mean"] for m in r.index}, **{m + "_ci": r.loc[m, "ci95"] for m in r.index}})
R = pd.DataFrame(rows); R.to_csv("scenario_results.csv", index=False)
print(R[["scenario","mean_wait","mean_wait_ci","p90_wait","hi_acuity_wait","peak_waiting","still_waiting","treated","mean_util","peak_util"]].round(1).to_string())
fig, ax = plt.subplots(figsize=(9, 4.8)); ax.barh(R.scenario, R.mean_wait, xerr=R.mean_wait_ci, color="#1f77b4")
ax.invert_yaxis(); ax.set_xlabel("Mean wait (min); 30 runs, 95% CI"); fig.tight_layout(); fig.savefig("chart_wait.png", dpi=150)
fig, ax = plt.subplots(figsize=(9, 4.8))
for k in ["Normal operations", "Reduced staffing + EHR outage (90 min)", "Surge + callouts + EHR outage"]:
    ax.plot(run(S[k])["timeline"].waiting, label=k)
ax.set_xlabel("Minute of shift"); ax.set_ylabel("Patients waiting"); ax.legend(); fig.tight_layout(); fig.savefig("chart_queue.png", dpi=150)
