import csv
from job_finder import JobFinder
from cache_utils import get_cache_key, load_cache, save_cache

_all__ = ["job_scanner"]

# Fields to include in the final output
EXPORT_FIELDS = ["Description", "Link", "Location", "Published At", "Full Description"]


def _trim_jobs(jobs):
    """Return jobs with only selected fields."""
    return [{k: v for k, v in job.items() if k in EXPORT_FIELDS} for job in jobs]


def _save_to_csv(jobs, filename="jobs.csv"):
    """Export filtered job listings to a CSV file with predefined columns."""
    if not jobs:
        print("No jobs to save.")
        return
    try:
        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=EXPORT_FIELDS)
            writer.writeheader()
            for job in jobs:
                writer.writerow({h: job.get(h, "") for h in EXPORT_FIELDS})
        print(f" Saved {len(jobs)} jobs to {filename}")
    except PermissionError:
        print("⚠ Could not save CSV. Make sure the file isn't open in Excel.")
    except Exception as e:
        print(f" Failed to save CSV: {e}")


def job_scanner(roles, levels, locations, sort_by="location", limit=100, csv_filename="jobs.csv"):
    """
    Public interface to run a full job search pipeline:
    - Aggregates job postings from multiple sources
    - Filters and deduplicates them
    - Sorts by user-defined preference
    - Saves the result to CSV

    Args:
        roles (List[str]): Main role to match in job descriptions.
        levels (List[str]): Additional keywords to refine results. If 'none', defaults to first_keywords.
        locations (List[str]): Preferred locations (e.g., ["israel", "remote"]).
        sort_by (str): Sorting field — "location", "keyword", or "published at".
        limit (int): Max jobs to fetch from each source.

    Returns:
        List[Dict]: Final trimmed job entries (also saved to 'jobs.csv').
    """
    sort_by = sort_by.strip().lower()
    print("Scanning jobs...")

    finder = JobFinder(roles, levels, locations, limit=limit)
    raw = finder.get_raw()

    # Load cached results if available
    cache_key = get_cache_key(roles, levels, locations, limit)
    cached = load_cache(cache_key)

    if cached:
        print("Using cached data...")
        finder.set_raw(cached)
    else:
        finder.aggregate()
        save_cache(cache_key, raw)

    # Filter and sort
    matched = finder.filter_and_dedupe()

    sort_preferences = locations if sort_by == "location" else roles
    matched = JobFinder.sort_by_preference(matched, sort_by, sort_preferences)

    # Trim results and save to CSV
    trimmed = _trim_jobs(matched)
    print(f"{len(trimmed)} jobs matched your criteria.")
    _save_to_csv(trimmed, csv_filename)
