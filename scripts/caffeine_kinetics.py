import pandas as pd
import numpy as np
from pathlib import Path

INPUT = Path("results/coffee_summary.csv")
OUTPUT = Path("results/caffeine_decay.csv")


def main():
    df = pd.read_csv(INPUT)

    required_cols = ["name", "estimated_daily_caffeine_mg_clean"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(
                f"Missing required column: {col}. Found columns: {df.columns.tolist()}"
            )

    # toy first-order decay model
    # C(t) = C0 * exp(-k t)
    # not physiologically exact, just a teaching example
    k = 0.15  # per hour

    results = []
    for _, row in df.iterrows():
        name = row["name"]
        C0 = row["estimated_daily_caffeine_mg_clean"]

        c_2h = C0 * np.exp(-k * 2)
        c_5h = C0 * np.exp(-k * 5)
        c_10h = C0 * np.exp(-k * 10)

        results.append(
            {
                "name": name,
                "initial_caffeine_mg": round(C0, 2),
                "caffeine_after_2h_mg": round(c_2h, 2),
                "caffeine_after_5h_mg": round(c_5h, 2),
                "caffeine_after_10h_mg": round(c_10h, 2),
                "percent_remaining_after_10h": round(100 * np.exp(-k * 10), 2),
            }
        )

    out = pd.DataFrame(results)
    out.to_csv(OUTPUT, index=False)

    print("Caffeine kinetics calculated successfully ☕")
    print(out.head())


if __name__ == "__main__":
    main()
