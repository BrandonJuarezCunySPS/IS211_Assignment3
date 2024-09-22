import argparse
import csv
import re
from collections import Counter
from datetime import datetime
import requests
import io

#Download File Definition
def download_file(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return io.StringIO(response.text)  # Use StringIO to simulate a file object

#Process File Definition
def process_file(file):
    image_pattern = re.compile(r'\.(jpg|gif|png)$', re.IGNORECASE)
    browser_pattern = re.compile(r'(Firefox|Chrome|Internet Explorer|Safari)', re.IGNORECASE)

    image_hits = 0
    total_hits = 0
    browser_counts = Counter()
    hourly_hits = Counter()

    reader = csv.reader(file)
    for row in reader:
        if len(row) < 5:
            continue

        path, datetime_str, user_agent, status, size = row
        total_hits += 1

        # Check if the hit is an image
        if image_pattern.search(path):
            image_hits += 1

        # Count browser types
        browser_match = browser_pattern.search(user_agent)
        if browser_match:
            browser = browser_match.group()
            browser_counts[browser] += 1

        # Count hits by hour
        try:
            dt = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S")
            hour = dt.hour
            hourly_hits[hour] += 1
        except ValueError:
            continue

    return image_hits, total_hits, browser_counts, hourly_hits

#Extra Credit Code
def print_statistics(image_hits, total_hits, browser_counts, hourly_hits):
    if total_hits > 0:
        image_percentage = (image_hits / total_hits) * 100
        print(f"Image requests account for {image_percentage:.1f}% of all requests")

    if browser_counts:
        most_common_browser = browser_counts.most_common(1)[0]
        print(f"The most popular browser is {most_common_browser[0]} with {most_common_browser[1]} hits")

    for hour in range(24):
        print(f"Hour {hour:02d} has {hourly_hits.get(hour, 0)} hits")




def main(url):
    file = download_file(url)
    image_hits, total_hits, browser_counts, hourly_hits = process_file(file)
    print_statistics(image_hits, total_hits, browser_counts, hourly_hits)
    print(f"Running main with URL = {url}...")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
