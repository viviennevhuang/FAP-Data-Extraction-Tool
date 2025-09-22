import json
import pandas as pd
from pathlib import Path

def swf_json_to_csv(json_path: str, output_dir: str = "csv_outputs"):
    # Load JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # --- General Info ---
    general_info = []
    for item in data:
        name = f"{item.get('fund_name')} {item.get('reporting_period', {}).get('value')}"
        general_info.append({
            "fund_name": name,
            #"fund_name": item.get("fund_name"),
            "country": item.get("country"),
            "reporting_period": item.get("reporting_period", {}).get("value"),
            "reporting_clarification": item.get("reporting_period", {}).get("clarification"),
            "investment_horizon": item.get("investment_horizon"),
            "assets_under_management": item.get("assets_under_management", {}).get("value") if item.get("assets_under_management") else None,
            "aum_currency": item.get("assets_under_management", {}).get("currency") if item.get("assets_under_management") else None
        })
    pd.DataFrame(general_info).to_csv(f"{output_dir}/general_info.csv", index=False)

    # --- Investment Mandate ---
    mandate = []
    for item in data:
        name = f"{item.get('fund_name')} {item.get('reporting_period', {}).get('value')}"
        mandate.append({
            "fund_name": name,
            "investment_horizon": item.get("investment_horizon"),
            "investment_mandate": item.get("investment_mandate")
        })
    pd.DataFrame(mandate).to_csv(f"{output_dir}/mandate.csv", index=False)

    # --- Annual Returns ---
    returns = []
    for item in data:
        name = f"{item.get('fund_name')} {item.get('reporting_period', {}).get('value')}"
        for ret in item.get("annual_return_percent", []):
            returns.append({
                "fund_name": name,
                **ret
            })
    pd.DataFrame(returns).to_csv(f"{output_dir}/annual_returns.csv", index=False)

    # --- Benchmarks ---
    benchmarks = []
    for item in data:
        name = f"{item.get('fund_name')} {item.get('reporting_period', {}).get('value')}"
        for bm in item.get("benchmark_comparison", []) or []:
            benchmarks.append({
                "fund_name": name,
                **bm
            })
    if benchmarks:
        pd.DataFrame(benchmarks).to_csv(f"{output_dir}/benchmarks.csv", index=False)

    # --- Metrics ---
    metrics_records = []
    for item in data:
        name = f"{item.get('fund_name')} {item.get('reporting_period', {}).get('value')}"
        metrics = item.get("metrics", {})
        if metrics:
            for metric_name, metric_values in metrics.items():
                if metric_values:
                    for m in metric_values:
                        metrics_records.append({
                            "fund_name": name,
                            "metric_type": metric_name,
                            "value": m.get("value"),
                            "time_period": m.get("time_period"),
                            "clarification": m.get("metric_clarification")
                        })
    if metrics_records:
        pd.DataFrame(metrics_records).to_csv(f"{output_dir}/metrics.csv", index=False)

    # --- Asset Allocation ---
    asset_alloc = []
    for item in data:
        name = f"{item.get('fund_name')} {item.get('reporting_period', {}).get('value')}"
        aa = item.get("asset_allocation", {})
        asset_alloc.append({
            "fund_name": name,
            **aa
        })
    pd.DataFrame(asset_alloc).to_csv(f"{output_dir}/asset_allocation.csv", index=False)

    # --- Investment Geography ---
    geography = []
    for item in data:
        name = f"{item.get('fund_name')} {item.get('reporting_period', {}).get('value')}"
        for geo in item.get("investment_geography", []) or []:
            geography.append({
                "fund_name": name,
                **geo
            })
    if geography:
        pd.DataFrame(geography).to_csv(f"{output_dir}/geography.csv", index=False)

    # --- Management Costs ---
    mgmt_costs = []
    for item in data:
        name = f"{item.get('fund_name')} {item.get('reporting_period', {}).get('value')}"
        mc = item.get("management_costs", {})
        if mc:
            mgmt_costs.append({
                "fund_name": name,
                **mc
            })
    if mgmt_costs:
        pd.DataFrame(mgmt_costs).to_csv(f"{output_dir}/management_costs.csv", index=False)

    print(f"CSV files written to {output_dir}")

# Example usage:
swf_json_to_csv("output3.json")
