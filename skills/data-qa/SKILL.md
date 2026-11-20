---
name: data-qa
description: Profiles and sanity-checks a CSV or spreadsheet before any analysis touches it. Reports row and column counts, column types, blanks, duplicate keys, outliers, date ranges, and whether totals foot, then gives a ready-or-not verdict with the fixes needed. Use when the user receives a new data drop, says "check this data", "is this clean", "before I build on this", or whenever another skill is about to compute on a file nobody has inspected.
license: MIT. See LICENSE in the repository root.
metadata:
  author: Echoed Words LLC
  kit: agentic-analyst-kit
  version: "1.0"
---

# Data QA

You inspect a dataset and tell the analyst whether it is safe to build on. The output is a short profile, a list of problems ranked by how badly they would distort an analysis, and one verdict: **Ready**, **Ready with caveats**, or **Not ready**.

Run this before `variance-analysis`, `recurring-report`, or `forecast-stress-test` whenever the file is new or changed.

## Steps

1. **Profile the file.** If `scripts/profile_csv.py` can run, use it (standard library only, no installs):

   ```
   python3 scripts/profile_csv.py data.csv [--key line_item] [--control-total 1234567 --total-col amount]
   ```

   It prints: rows, columns, each column's inferred type, blank count, distinct count, min/max (numeric and date), duplicates on the key, outliers by the 1.5 × IQR rule, and whether a control total matches. For an Excel file, export the sheet to CSV first or read it with whatever spreadsheet tool the environment provides; the checks are the same.

2. **Check the things a script cannot.** Read the headers and the first and last five rows and ask:
   - Is there a header row at all, and is it the first row?
   - Are there total or subtotal rows mixed into detail rows?
   - Do two columns mean the same thing under different names?
   - Are negative numbers written as parentheses, with minus signs, or both?
   - Are dates one format throughout? Does the period in the file match the period the user said?
   - Are there merged cells, notes rows, or a second table below the first (common in exported spreadsheets)?

3. **Reconcile.** If the user gave a control total, compare. If a total row exists, compare it to the sum of the detail rows. Report both numbers; never adjust either.

4. **Rank the problems.** Order by distortion risk: wrong period or wrong units first, then duplicate keys and mixed total rows, then blanks in numeric columns, then outliers, then cosmetic issues.

5. **Give the verdict and the fixes.** Each fix is one line the analyst can act on: which rows, which column, what to do. Where a fix changes numbers (removing a duplicate, excluding a total row), say how much the total changes.

## Output format

```
## Data QA: [file], [rows] rows x [columns] columns

Verdict: Ready with caveats

Profile
| Column | Type | Blanks | Distinct | Min | Max | Note |
| ... |

Problems (ranked)
1. [problem, where, effect on totals]
2. ...

Fixes before analysis
- [action]

Reconciliation
- File total [x]; computed total [y]; difference [z]
```

## Rules

- Never silently fix data. Report, propose, and let the analyst decide.
- Outliers are flagged, not removed; a true outlier is often the story.
- If a column type is ambiguous (IDs that look numeric, ZIP codes, account codes), treat it as text and say so. Account codes with leading zeros are the classic casualty.
- When the file is larger than you can read in full, profile with the script and say which rows you inspected by eye.
- If the data contains names, account numbers, health, or other regulated fields, stop and apply the `data-handling-guardrail` skill before continuing.

## Example verdicts

- **Ready**: no duplicate keys, no blanks in numeric columns, control total matches to the cent.
- **Ready with caveats**: a subtotal row was found and excluded (changes total by $48,200); three blank cost rows treated as zero.
- **Not ready**: the file's period is FY26 Q2 and the request is for Q3; 14 duplicate line keys would double-count $310,000.
