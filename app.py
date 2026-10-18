import streamlit as st, pandas as pd, plotly.express as px
from dataclasses import replace
from sim import Params, run, run_many, summarize, SCENARIOS

st.set_page_config(page_title="The Pitt ED Resilience Simulator", layout="wide")
st.title("The Pitt — Emergency Department Resilience Simulator")
st.caption("Synthetic, simplified model. Findings are simulation outputs, not clinical predictions.")

with st.sidebar:
    st.header("Conditions")
    p = Params(
        arrivals_per_hr=st.slider("Baseline arrivals / hour", 10, 40, 21),
        surge_patients=st.slider("Mass-casualty surge (patients at once)", 0, 60, 20),
        spaces=st.slider("Treatment spaces", 10, 50, 30),
        nurses=st.slider("Nurses on duty", 4, 20, 9),
        physicians=st.slider("Physicians on duty", 1, 8, 4),
        nurse_callouts=st.slider("Nurse call-outs (mid-shift)", 0, 6, 2),
        downtime_min=st.slider("EHR outage (minutes)", 0, 240, 90, step=15),
        seed=st.number_input("Random seed", value=42))
    n_runs = st.slider("Replicate runs per case", 1, 50, 20)
    st.header("Response strategy")
    strat = dict(
        surge_capacity=st.checkbox("Activate surge capacity (+6 spaces)"),
        reallocate_staff=st.checkbox("Reallocate staff (+2 nurses)"),
        prioritize_acuity=st.checkbox("Prioritize high acuity", value=True),
        downtime_procedure=st.checkbox("Downtime documentation procedure"))

base = replace(p, surge_patients=0, nurse_callouts=0, downtime_min=0, **{k: False for k in strat if k != "prioritize_acuity"})
cases = {"Baseline (no stressors)": base, "Stressed, no response": replace(p, surge_capacity=False, reallocate_staff=False,
         downtime_procedure=False, prioritize_acuity=False), "Stressed + chosen response": replace(p, **strat)}
res = {k: run(v) for k, v in cases.items()}

m = pd.DataFrame({k: summarize(run_many(v, n_runs))["mean"] for k, v in cases.items()}).T
m.columns = ["Arrivals", "Seen", "Treated", "Still waiting", "Mean wait", "P90 wait", "ESI 1-2 wait",
             "Peak waiting", "Mean util.", "Peak util."]
st.subheader(f"Scenario comparison (mean of {n_runs} runs)")
st.dataframe(m.round(2), use_container_width=True)

tl = pd.concat([v["timeline"].assign(case=k) for k, v in res.items()])
c1, c2 = st.columns(2)
c1.plotly_chart(px.line(tl, x="minute", y="waiting", color="case", title="Patients waiting"), use_container_width=True)
c2.plotly_chart(px.line(tl, x="minute", y="utilization", color="case", title="Treatment-capacity utilization"), use_container_width=True)
c1.plotly_chart(px.bar(m.reset_index(), x="index", y=["Mean wait", "P90 wait"], barmode="group",
                       title="Wait (min)", labels={"index": ""}), use_container_width=True)
c2.plotly_chart(px.bar(m.reset_index(), x="index", y="Treated", title="Patients treated by end of shift",
                       labels={"index": ""}), use_container_width=True)

st.subheader("Preset scenarios")
if st.button("Run all presets"):
    rows = {k: summarize(run_many(v, n_runs))["mean"] for k, v in SCENARIOS.items()}
    st.dataframe(pd.DataFrame(rows).T.round(2), use_container_width=True)
st.info("Limitations: synthetic parameters, simplified provider/bed/nurse logic, no clinical validation.")
