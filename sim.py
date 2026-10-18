"""Minute-step ED flow simulator (synthetic, educational). Not a clinical model."""
from dataclasses import dataclass, field
import numpy as np, pandas as pd

ESI_P = [0.03, 0.17, 0.40, 0.28, 0.12]           # ESI 1..5 mix (illustrative)
TX_MEAN = [90, 80, 55, 25, 15]                    # mean treatment min by ESI
EVAL_MEAN = [6, 8, 10, 8, 6]                      # provider-evaluation min by ESI

@dataclass
class Params:
    arrivals_per_hr: float = 21.0
    surge_patients: int = 0          # extra patients arriving at once
    surge_minute: int = 180
    spaces: int = 30
    nurses: int = 9
    physicians: int = 4
    nurse_callouts: int = 0
    callout_minute: int = 120
    patients_per_nurse: float = 3.0
    eval_scale: float = 1.25         # calibrated provider-evaluation multiplier
    downtime_min: int = 0
    downtime_minute: int = 240
    downtime_slowdown: float = 1.5   # eval/treatment multiplier during EHR outage
    horizon: int = 720
    # response strategies
    surge_capacity: bool = False     # +6 spaces, 30 min after surge/outage trigger
    reallocate_staff: bool = False   # +2 nurses, 30 min after trigger
    prioritize_acuity: bool = True   # False = FIFO
    downtime_procedure: bool = False # cuts slowdown to 1.2
    seed: int = 42

def run(p: Params) -> dict:
    rng = np.random.default_rng(p.seed)
    pts, queue, active = [], [], []   # active: [end_time, idx]
    prov_free = [0] * p.physicians    # minute each physician becomes free
    trigger = None
    if p.surge_patients: trigger = p.surge_minute
    if p.downtime_min: trigger = min(trigger or 10**9, p.downtime_minute)
    ts = []
    for t in range(p.horizon):
        n = rng.poisson(p.arrivals_per_hr / 60) + (p.surge_patients if t == p.surge_minute else 0)
        for _ in range(n):
            esi = rng.choice(5, p=ESI_P)
            pts.append(dict(arrive=t, esi=esi + 1, start=None, end=None,
                            tx=max(5, rng.gamma(4, TX_MEAN[esi] / 4)), ev=max(2, rng.gamma(4, p.eval_scale * EVAL_MEAN[esi] / 4))))
            queue.append(len(pts) - 1)
        down = p.downtime_min and p.downtime_minute <= t < p.downtime_minute + p.downtime_min
        slow = (1.2 if p.downtime_procedure else p.downtime_slowdown) if down else 1.0
        spaces, nurses = p.spaces, p.nurses
        if t >= p.callout_minute: nurses -= p.nurse_callouts
        if trigger is not None and t >= trigger + 30:
            spaces += 6 if p.surge_capacity else 0
            nurses += 2 if p.reallocate_staff else 0
        cap = min(spaces, max(nurses, 0) * p.patients_per_nurse)
        active = [a for a in active if a[0] > t]
        order = sorted(queue, key=lambda i: (pts[i]["esi"], pts[i]["arrive"])) if p.prioritize_acuity else queue
        for i in order:
            free = [k for k, f in enumerate(prov_free) if f <= t]
            if not free or len(active) >= cap: break
            ev = pts[i]["ev"] * slow
            prov_free[free[0]] = t + ev
            pts[i]["start"] = t
            pts[i]["end"] = t + ev + pts[i]["tx"] * slow
            active.append([pts[i]["end"], i]); queue.remove(i)
        ts.append(dict(minute=t, waiting=len(queue), in_treatment=len(active), capacity=cap,
                       utilization=len(active) / cap if cap else 1.0, downtime=int(bool(down))))
    df = pd.DataFrame(pts); tl = pd.DataFrame(ts)
    seen = df.dropna(subset=["start"]).assign(wait=lambda d: d.start - d.arrive)
    # patients still waiting at end are censored: count their wait so far
    still = df[df.start.isna()].assign(wait=lambda d: p.horizon - d.arrive)
    allw = pd.concat([seen, still])
    hi = allw[allw.esi <= 2]
    return dict(patients=df, timeline=tl, metrics=dict(
        arrivals=len(df), seen=len(seen), treated=int((df.end <= p.horizon).sum()),
        still_waiting=len(still), mean_wait=allw.wait.mean(), p90_wait=allw.wait.quantile(.9),
        hi_acuity_wait=hi.wait.mean() if len(hi) else float("nan"),
        peak_waiting=int(tl.waiting.max()), mean_util=tl.utilization.mean(), peak_util=tl.utilization.max()))

SCENARIOS = {
    "Normal operations": Params(),
    "Reduced staffing (2 callouts)": Params(nurse_callouts=2, nurses=9),
    "Reduced staffing + EHR outage (90 min)": Params(nurse_callouts=2, downtime_min=90),
    "Mass-casualty surge (+20 at once)": Params(surge_patients=20),
    "Surge + callouts + EHR outage": Params(surge_patients=20, nurse_callouts=2, downtime_min=90),
}


from dataclasses import replace as _rep
def run_many(p: Params, n: int = 30) -> pd.DataFrame:
    """Replicate over seeds; returns one metrics row per seed."""
    return pd.DataFrame([run(_rep(p, seed=p.seed + i))["metrics"] for i in range(n)])

def summarize(reps: pd.DataFrame) -> pd.DataFrame:
    m, se = reps.mean(), reps.sem()
    return pd.DataFrame({"mean": m, "ci95": 1.96 * se})
