"""Serialize validation outcomes into portable JSON and CSV artifacts."""
import csv, json
from pathlib import Path

FIELDS = ["record_type", "record_id", "row_number", "field", "error_type", "detail"]
def write_reports(output, count, profile, seed, customers, orders, issues):
    out = Path(output); out.mkdir(parents=True, exist_ok=True)
    summary = {"profile":profile, "seed":seed, "customers_generated":len(customers),
               "orders_generated":len(orders), "issue_count":len(issues),
               "customers_with_issues":len({i["row_number"] for i in issues if i["record_type"]=="customer"}),
               "orders_with_issues":len({i["row_number"] for i in issues if i["record_type"]=="order"}),
               "status":"PASS" if not issues else "FAIL"}
    (out / "validation-summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    with (out / "validation-issues.csv").open("w", newline="", encoding="utf-8") as stream:
        writer=csv.DictWriter(stream, fieldnames=FIELDS); writer.writeheader(); writer.writerows(issues)
    return summary
