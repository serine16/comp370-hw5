#!/usr/bin/env python3
import argparse
import csv
from collections import defaultdict
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(
        description="CLI tool to output the number of each complaint type per borough for a given date range."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input CSV file")
    parser.add_argument("-s", "--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("-e", "--end", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("-o", "--output", help="Path to optional output CSV file")

    args = parser.parse_args()

    start_date = datetime.strptime(args.start, "%Y-%m-%d")
    end_date = datetime.strptime(args.end, "%Y-%m-%d")

    # Dictionary to store counts: {(complaint_type, borough): count}
    counts = defaultdict(int)

    # Opening and processing the CSV file line-by-line using index positions
    with open(args.input, mode="r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # Skip header row
        
        for row in reader:
            if len(row) <= 25:
                continue
            
            date_str = row[1].strip()
            complaint_type = row[5].strip()
            borough = row[25].strip()

            if not date_str or not complaint_type or not borough:
                continue
                
            try:
                # Handle standard NYC Open Data format (e.g., '01/01/2024 12:00:00 AM')
                date_part = date_str.split()[0]
                if "/" in date_part:
                    incident_date = datetime.strptime(date_part, "%m/%d/%Y")
                else:
                    incident_date = datetime.strptime(date_part, "%Y-%m-%d")
            except ValueError:
                continue

            # Check if incident date falls within the range
            if start_date <= incident_date <= end_date:
                counts[(complaint_type, borough)] += 1

    # Preparing output rows
    output_rows = []
    for (comp_type, borough), count in sorted(counts.items()):
        output_rows.append({"complaint type": comp_type, "borough": borough, "count": count})

    fieldnames = ["complaint type", "borough", "count"]

    if args.output:
        with open(args.output, mode="w", newline="", encoding="utf-8") as out_f:
            writer = csv.DictWriter(out_f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(output_rows)
    else:
        # Display results to stdout in CSV format
        print("complaint type, borough, count")
        for row in output_rows:
            print(f"{row['complaint type']}, {row['borough']}, {row['count']}")

if __name__ == "__main__":
    main()


