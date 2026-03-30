import pandas as pd
from pathlib import Path

INPUT = Path("data/coffee_team.csv")
OUT_SUMMARY = Path("results/coffee_summary.csv")
OUT_TOP = Path("results/top_consumer.txt")


def classify_consumer(mg: float) -> str:
    if mg < 150:
        return "mildly caffeinated"
    elif mg < 350:
        return "functional chemist"
    elif mg < 600:
        return "deadline mode"
    else:
        return "instrument-day survival"


def main():
    df = pd.read_csv(INPUT)

    # clean obviously impossible values for a funny but robust tutorial
    df["cups_per_day_clean"] = df["cups_per_day"].clip(lower=0, upper=20)
    df["estimated_daily_caffeine_mg_clean"] = (
        df["cups_per_day_clean"] * df["caffeine_mg_per_cup"]
    )

    df["consumer_class"] = df["estimated_daily_caffeine_mg_clean"].apply(
        classify_consumer
    )

    # keep one row per person so the next Snakemake rule can model kinetics per person
    summary = df[
        [
            "name",
            "coffee_style",
            "cups_per_day",
            "cups_per_day_clean",
            "caffeine_mg_per_cup",
            "estimated_daily_caffeine_mg",
            "estimated_daily_caffeine_mg_clean",
            "descriptor_score",
            "messiness_index",
            "consumer_class",
            "descriptors",
        ]
    ].copy()

    summary.to_csv(OUT_SUMMARY, index=False)

    top = summary.sort_values(
        "estimated_daily_caffeine_mg_clean", ascending=False
    ).iloc[0]
    OUT_TOP.write_text(
        f"Top coffee consumer: {top['name']}\n"
        f"Style: {top['coffee_style']}\n"
        f"Corrected estimated daily caffeine: {top['estimated_daily_caffeine_mg_clean']} mg\n"
        f"Consumer class: {top['consumer_class']}\n"
        f"Descriptors: {top['descriptors']}\n"
    )


if __name__ == "__main__":
    main()
