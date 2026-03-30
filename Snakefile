rule all:
    input:
        "results/coffee_summary.csv",
        "results/top_consumer.txt",
        "results/caffeine_decay.csv"


rule analyze_coffee:
    input:
        "data/coffee_team.csv"
    output:
        "results/coffee_summary.csv",
        "results/top_consumer.txt"
    shell:
        "python scripts/analyze_coffee.py"


rule caffeine_kinetics:
    input:
        "results/coffee_summary.csv"
    output:
        "results/caffeine_decay.csv"
    shell:
        "python scripts/caffeine_kinetics.py"