import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "synthetic_patient_flow.csv")
df["arrival_time"] = pd.to_datetime(df["arrival_time"])

print("Rows:", len(df))
print("Median wait:", round(df["triage_to_provider_min"].median(), 1), "minutes")
print("90th percentile wait:", round(df["triage_to_provider_min"].quantile(.90), 1), "minutes")
print("Average arrivals per shift-hour:", round(len(df) / 24, 1))

print("\nWait by acuity:")
print(df.groupby("triage_acuity_esi")["triage_to_provider_min"].agg(["count","median","mean"]).round(1))

print("\nWait by operational flag:")
print(df.groupby(["mass_casualty_related_flag","ehr_downtime_flag"])["triage_to_provider_min"].agg(["count","median","mean"]).round(1))

# Chart 1: hourly arrivals and median waits
hourly = pd.read_csv(ROOT / "hourly_metrics.csv")
for shift, g in hourly.groupby("simulated_shift"):
    fig, ax1 = plt.subplots()
    ax1.bar(g["hour_of_shift"], g["arrivals"])
    ax1.set_xlabel("Hour of simulated shift")
    ax1.set_ylabel("Patient arrivals")
    ax1.set_title(f"{shift}: arrivals and median wait")
    ax2 = ax1.twinx()
    ax2.plot(g["hour_of_shift"], g["median_wait_min"], marker="o")
    ax2.set_ylabel("Median wait (minutes)")
    fig.tight_layout()
    fig.savefig(ROOT / f"{shift.lower()}_arrivals_waits.png", dpi=160)
    plt.close(fig)

# Chart 2: wait distribution by acuity
order = ["ESI_1","ESI_2","ESI_3","ESI_4","ESI_5"]
data = [df.loc[df["triage_acuity_esi"] == x, "triage_to_provider_min"] for x in order]
fig, ax = plt.subplots()
ax.boxplot(data, tick_labels=order)
ax.set_xlabel("Synthetic triage acuity label")
ax.set_ylabel("Triage-to-provider time (minutes)")
ax.set_title("Wait-time distribution by acuity")
fig.tight_layout()
fig.savefig(ROOT / "wait_by_acuity.png", dpi=160)
plt.close(fig)
