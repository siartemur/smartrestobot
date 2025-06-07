import pandas as pd

METRICS_FILE = "app/logs/metrics.csv"

def generate_ab_test_report():
    if not pd.io.common.file_exists(METRICS_FILE):
        return {"error": "metrics.csv not found."}

    df = pd.read_csv(METRICS_FILE, header=None)
    df.columns = [
        "timestamp", "restaurant_id", "user_id", "agent_type", "prompt_version",
        "model", "prompt_length", "response_length", "token_usage",
        "latency_ms", "is_bad_response"
    ]

    ab_df = df[df["agent_type"] == "ab_test"]

    if ab_df.empty:
        return {"error": "No A/B test data found in metrics.csv."}

    report = (
        ab_df
        .groupby("prompt_version")
        .agg({
            "latency_ms": "mean",
            "token_usage": "mean",
            "is_bad_response": "mean"
        })
        .rename(columns={
            "latency_ms": "avg_latency_ms",
            "token_usage": "avg_token_usage",
            "is_bad_response": "bad_response_rate"
        })
        .reset_index()
    )

    # Yüzde formatına çevirelim
    report["bad_response_rate"] = (report["bad_response_rate"] * 100).round(2)

    return report.to_dict(orient="records")
