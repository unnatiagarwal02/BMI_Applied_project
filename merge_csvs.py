#!/usr/bin/env python3
"""Merge two CSVs by vertical concatenation (union of columns) and save output.

Usage:
  python3 merge_csvs.py 
  python3 merge_csvs.py --a Cleaning_data_cleaned.csv --b Cleaning_data_merged_17_18.csv -o Cleaning_data_merged_combined.csv
"""
import argparse
from pathlib import Path
import sys

try:
    import pandas as pd
except Exception as e:
    print("pandas is required. Install with: pip install pandas")
    raise


def load_csv(path: Path):
    return pd.read_csv(path, dtype=object)


def main():
    p = argparse.ArgumentParser(description="Concatenate two CSVs (union columns) and save result")
    p.add_argument('--a', default='Cleaning_data_cleaned.csv', help='First input CSV')
    p.add_argument('--b', default='Cleaning_data_merged_17_18.csv', help='Second input CSV')
    p.add_argument('-o', '--out', default='Cleaning_data_merged_combined.csv', help='Output CSV path')
    args = p.parse_args()

    a = Path(args.a)
    b = Path(args.b)
    out = Path(args.out)

    missing = [str(x) for x in (a,b) if not x.exists()]
    if missing:
        print('Missing input files:', ', '.join(missing))
        sys.exit(2)

    df1 = load_csv(a)
    df2 = load_csv(b)

    combined = pd.concat([df1, df2], ignore_index=True, sort=False)
    combined.to_csv(out, index=False)

    print(f"Wrote {out} — rows: {len(combined)} (from {len(df1)} + {len(df2)}), columns: {len(combined.columns)}")

if __name__ == '__main__':
    main()
