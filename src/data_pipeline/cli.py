"""Command-line interface."""
import argparse, json, os, sys
from .generator import generate
from .validation import validate, valid_customers, valid_orders
from .reports import write_reports

def main(argv=None):
    parser=argparse.ArgumentParser(prog="data-pipeline", description="Generate, validate, report, and optionally persist test fixtures.")
    sub=parser.add_subparsers(dest="command", required=True)
    run=sub.add_parser("run", help="generate and validate a fixture batch")
    run.add_argument("--count", type=int, default=500)
    run.add_argument("--profile", choices=["standard", "edge-cases"], default="standard")
    run.add_argument("--seed", type=int, default=42)
    run.add_argument("--output", default="reports")
    run.add_argument("--persist", action="store_true")
    args=parser.parse_args(argv)
    try:
        customers, orders=generate(args.count,args.profile,args.seed)
        issues=validate(customers,orders)
        summary=write_reports(args.output,args.count,args.profile,args.seed,customers,orders,issues)
        if args.persist:
            url=os.getenv("DATABASE_URL")
            if not url: raise ValueError("--persist requires DATABASE_URL")
            from .database import persist
            persist(url,valid_customers(customers,issues),valid_orders(orders,issues))
            summary["persisted"]=True
        print(json.dumps(summary,indent=2))
        return 0 if not issues else 2
    except Exception as exc:
        print(f"data-pipeline: {exc}",file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
