#!/usr/bin/env python3
"""Profile a CSV before analysis. Standard library only.

Usage:
  python3 profile_csv.py FILE.csv [--key COL] [--control-total N --total-col COL]
                                  [--sample 5] [--json]

Reports rows, columns, inferred types, blanks, distinct counts, min/max,
duplicate keys, IQR outliers, and a control-total check.
"""
import argparse
import csv
import json
import re
import statistics
import sys
from datetime import datetime

DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d-%b-%Y", "%b %d, %Y", "%Y/%m/%d", "%Y-%m")


def parse_num(s):
    t = s.strip().replace(",", "").replace("$", "").replace("%", "")
    if t == "":
        return None
    neg = t.startswith("(") and t.endswith(")")
    if neg:
        t = t[1:-1]
    try:
        n = float(t)
    except ValueError:
        return None
    return -n if neg else n


def parse_date(s):
    t = s.strip()
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(t, f)
        except ValueError:
            continue
    return None


def looks_like_code(values):
    """IDs, ZIPs, account codes: numeric-looking but not quantities."""
    vals = [v for v in values if v.strip()]
    if not vals:
        return False
    leading_zero = sum(1 for v in vals if re.fullmatch(r"0\d+", v.strip()))
    fixed_len = len({len(v.strip()) for v in vals}) == 1 and len(vals[0].strip()) >= 5
    return leading_zero > 0 or fixed_len


def infer(values):
    nonblank = [v for v in values if v.strip() != ""]
    if not nonblank:
        return "empty", []
    nums = [parse_num(v) for v in nonblank]
    if all(n is not None for n in nums):
        if looks_like_code(nonblank):
            return "code (text)", []
        return "number", nums
    dates = [parse_date(v) for v in nonblank]
    if all(d is not None for d in dates):
        return "date", dates
    if all(v.strip().lower() in ("true", "false", "yes", "no", "y", "n") for v in nonblank):
        return "boolean", []
    numeric_share = sum(1 for n in nums if n is not None) / len(nonblank)
    if numeric_share >= 0.8:
        return "number (mixed; %d non-numeric)" % sum(1 for n in nums if n is None), [n for n in nums if n is not None]
    return "text", []


def iqr_outliers(nums):
    if len(nums) < 8:
        return []
    q = statistics.quantiles(nums, n=4)
    q1, q3 = q[0], q[2]
    iqr = q3 - q1
    if iqr == 0:
        return []
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return [n for n in nums if n < lo or n > hi]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file")
    p.add_argument("--key", help="column expected to be unique per row")
    p.add_argument("--control-total", type=float, help="expected total of --total-col")
    p.add_argument("--total-col", help="numeric column to sum for the control total")
    p.add_argument("--sample", type=int, default=5)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    with open(a.file, newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        rows = [r for r in reader]
    if not rows:
        sys.exit("error: empty file")
    header, body = rows[0], rows[1:]
    width = len(header)
    ragged = [i + 2 for i, r in enumerate(body) if len(r) != width]
    body = [r + [""] * (width - len(r)) if len(r) < width else r[:width] for r in body]

    TOTAL_WORDS = ("total", "grand total", "subtotal", "sum")
    total_like = [i + 2 for i, r in enumerate(body) if r and r[0].strip().lower() in TOTAL_WORDS]
    detail = [r for r in body if not (r and r[0].strip().lower() in TOTAL_WORDS)]

    print(f"## Data QA: {a.file}, {len(body)} rows x {width} columns"
          + (f" ({len(total_like)} total row(s) excluded from the profile)" if total_like else "") + "\n")
    problems = []
    if ragged:
        problems.append(f"{len(ragged)} rows have a different number of fields than the header (first at line {ragged[0]})")
    blank_headers = [i + 1 for i, h in enumerate(header) if not h.strip()]
    if blank_headers:
        problems.append(f"blank header in column(s) {blank_headers}; the header row may not be row 1")
    body = detail

    print("Profile")
    print("| Column | Type | Blanks | Distinct | Min | Max | Note |")
    print("| --- | --- | ---: | ---: | --- | --- | --- |")
    summary = {}
    for ci, name in enumerate(header):
        col = [r[ci] for r in body]
        blanks = sum(1 for v in col if v.strip() == "")
        distinct = len({v.strip() for v in col if v.strip() != ""})
        kind, parsed = infer(col)
        mn = mx = ""
        note = ""
        if kind.startswith("number") and parsed:
            mn, mx = f"{min(parsed):,.2f}", f"{max(parsed):,.2f}"
            out = iqr_outliers(parsed)
            if out:
                note = f"{len(out)} IQR outlier(s), e.g. {out[0]:,.2f}"
            if min(parsed) < 0 and name.lower() in ("plan", "actual", "amount", "cost", "spend", "budget"):
                note = (note + "; " if note else "") + "negative values present; check sign convention"
        elif kind == "date" and parsed:
            mn, mx = min(parsed).date().isoformat(), max(parsed).date().isoformat()
        elif kind == "code (text)":
            note = "looks like an ID or code; keep as text"
        if blanks:
            problems.append(f"'{name}': {blanks} blank value(s)")
        summary[name] = {"type": kind, "blanks": blanks, "distinct": distinct, "min": mn, "max": mx}
        print(f"| {name} | {kind} | {blanks} | {distinct} | {mn} | {mx} | {note} |")

    if total_like:
        problems.insert(0, f"total/subtotal row(s) mixed into detail at line(s) {total_like}; exclude before summing")

    if a.key:
        if a.key not in header:
            problems.append(f"key column '{a.key}' not found")
        else:
            ki = header.index(a.key)
            seen, dups = {}, []
            for r in body:
                k = r[ki].strip()
                seen[k] = seen.get(k, 0) + 1
            dups = [k for k, c in seen.items() if c > 1 and k != ""]
            if dups:
                problems.insert(0, f"{len(dups)} duplicate key(s) in '{a.key}', e.g. {dups[:3]}")

    recon = None
    if a.total_col:
        if a.total_col not in header:
            problems.append(f"total column '{a.total_col}' not found")
        else:
            ti = header.index(a.total_col)
            nums = [parse_num(r[ti]) for r in body]
            computed = sum(n for n in nums if n is not None)
            recon = {"computed": computed}
            if a.control_total is not None:
                diff = computed - a.control_total
                recon.update({"control": a.control_total, "difference": diff})
                if abs(diff) > 0.005:
                    problems.insert(0, f"control total mismatch: computed {computed:,.2f} vs control {a.control_total:,.2f} (difference {diff:+,.2f})")

    print("\nProblems (ranked)")
    if problems:
        for i, pr in enumerate(problems, 1):
            print(f"{i}. {pr}")
    else:
        print("none found by the script; still read the first and last rows by eye")

    if recon:
        print("\nReconciliation")
        print(f"- computed total of '{a.total_col}': {recon['computed']:,.2f}")
        if "control" in recon:
            print(f"- control total: {recon['control']:,.2f}; difference {recon['difference']:+,.2f}")

    print(f"\nFirst {a.sample} rows")
    for r in body[: a.sample]:
        print("- " + " | ".join(r))
    print(f"\nLast {a.sample} rows")
    for r in body[-a.sample:]:
        print("- " + " | ".join(r))

    verdict = "Ready" if not problems else ("Not ready" if any(w in problems[0] for w in ("duplicate", "mismatch", "total/subtotal")) else "Ready with caveats")
    print(f"\nVerdict (script view): {verdict}. The analyst confirms period, units and column meaning by eye.")
    if a.json:
        print(json.dumps({"rows": len(body), "columns": width, "profile": summary, "problems": problems, "reconciliation": recon, "verdict": verdict}))


if __name__ == "__main__":
    main()
