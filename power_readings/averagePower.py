#!/usr/bin/env python3
"""Calculate average power from CSV files."""

import csv
import os
import sys
from pathlib import Path
from datetime import datetime


def calculate_average_power(csv_file):
    """Calculate average power from a CSV file."""
    try:
        with open(csv_file, 'r') as f:
            # Skip header comments (lines starting with #)
            reader = csv.DictReader((line for line in f if not line.startswith('#')))
            power_values = [float(row['Power']) for row in reader if row['Power']]
            
            if power_values:
                return sum(power_values) / len(power_values)
            else:
                return None
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        return None


def process_directory(directory, output_file=None):
    """Process all CSV files in a directory."""
    csv_files = sorted(Path(directory).glob('**/*.csv'))
    
    if not csv_files:
        print(f"No CSV files found in {directory}")
        return
    
    results = []
    for csv_file in csv_files:
        avg = calculate_average_power(csv_file)
        if avg is not None:
            results.append((csv_file.name, avg))
    
    # Print results
    print(f"\nAverage Power Readings ({len(results)} files):\n")
    print(f"{'Filename':<50} {'Average Power (W)':<20}")
    print("-" * 70)
    for filename, avg in results:
        print(f"{filename:<50} {avg:<20.8f}")
    
    # Save to CSV if output file specified
    if output_file:
        try:
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Average Power (W)'])
                for filename, avg in results:
                    writer.writerow([filename, avg])
            print(f"\nResults saved to: {output_file}")
        except Exception as e:
            print(f"Error writing to {output_file}: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 averagePower.py <directory|file> [output.csv]")
        sys.exit(1)
    
    path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    path = Path(path)
    
    if path.is_file() and path.suffix == '.csv':
        avg = calculate_average_power(path)
        if avg is not None:
            print(f"Average power: {avg:.8f} W")
            if output_file:
                try:
                    with open(output_file, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Filename', 'Average Power (W)'])
                        writer.writerow([path.name, avg])
                    print(f"Results saved to: {output_file}")
                except Exception as e:
                    print(f"Error writing to {output_file}: {e}")
    elif path.is_dir():
        process_directory(path, output_file)
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
