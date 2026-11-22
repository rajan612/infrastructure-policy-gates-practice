"""Inspect the synthetic inventory; write a machine-readable compliance report."""
import json
from pathlib import Path
from app.policy import build_report


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    inventory = json.loads((root / "sample_data" / "resources.json").read_text())
    report = build_report(inventory["resources"])
    output = root / "reports" / "policy-report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Validated {report['checked']} synthetic resources: "
          f"{report['passed']} pass, {report['failed']} fail")
    for item in report["results"]:
        for violation in item["violations"]:
            print(f"  FAIL: {violation}")
    print(f"Report written: {output}")
    return 0 if report["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
