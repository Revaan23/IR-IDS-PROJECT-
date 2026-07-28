"""
reduce_dataset.py
-----------------
Creates a lightweight development dataset.

If a CSV contains more than 50,000 rows,
only the first 50,000 rows are copied.

Otherwise the whole file is copied.

Uses Python's built-in CSV reader.
"""

from pathlib import Path
import csv

# =====================================================
# CONFIGURATION
# =====================================================

SOURCE_FOLDER = Path("datasets/raw/CSE-CIC-IDS2018")

DESTINATION_FOLDER = Path(
    "datasets/raw/CSE-CIC-IDS2018-50K"
)

MAX_ROWS = 50000

DESTINATION_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================

print("=" * 70)
print("IR-IDS Development Dataset Generator")
print("=" * 70)

csv_files = sorted(
    SOURCE_FOLDER.glob("*.csv")
)

for csv_file in csv_files:

    print(f"\nProcessing : {csv_file.name}")

    output_file = DESTINATION_FOLDER / csv_file.name

    rows_written = 0

    with open(
        csv_file,
        "r",
        encoding="utf-8",
        errors="ignore",
        newline=""
    ) as infile, open(
        output_file,
        "w",
        encoding="utf-8",
        newline=""
    ) as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header
        header = next(reader)
        writer.writerow(header)

        for row in reader:

            writer.writerow(row)

            rows_written += 1

            if rows_written >= MAX_ROWS:
                break

    print(f"Saved : {rows_written:,} rows")

print("\n" + "=" * 70)
print("Development Dataset Created Successfully")
print("=" * 70)

print(f"\nLocation : {DESTINATION_FOLDER}")