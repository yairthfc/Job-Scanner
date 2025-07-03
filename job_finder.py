# === Standard library ===
import re
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import json
import pandas as pd

# === Third-party ===
import requests

# === Local ===
import config

country_map = config.country_map


class JobFinder:
    def __init__(self, keywords, secondary_keywords, locations, limit=300):
        """
               Initialize a JobFinder instance.

               Parameters:
                   keywords (List[str]): Primary keywords to filter job titles/descriptions.
                   secondary_keywords (List[str]): Secondary keywords to further refine matches.
                   locations (List[str]): List of location names or country aliases for job search.
                   limit (int): Maximum number of results to fetch per API call (default: 300).

               Behavior:
                   - Converts all keywords and secondary_keywords to lowercase and strips whitespace.
                   - Normalizes each location to lowercase and strips whitespace, then expands country names
                     into ISO codes when possible (using country_map). The resulting list of locations
                     includes both the original normalized strings and any expanded country codes.
                   - Initializes an internal list `_raw` to store fetched job entries.
               """
        self.keywords = [k.lower().strip() for k in keywords]
        self.secondary_keywords = [k.lower().strip() for k in secondary_keywords]
        self.limit = limit
        self._raw = []

        normalized_contries = [loc.lower().strip() for loc in locations]
        expanded_codes = []
        for cleaned in normalized_contries:
            if cleaned in country_map:
                code = country_map[cleaned]  # e.g. "usa" → "us", "canada" → "ca"
                if code not in normalized_contries and code not in expanded_codes:
                    expanded_codes.append(code)
        self.locations = normalized_contries + expanded_codes

    # =============  PRIVATE HELPERS===============
    def get_raw(self):
        """Returns the raw job data before filtering or deduplication."""
        return self._raw

    def set_raw(self, data):
        """Set the internal raw job data (used when loading from cache)."""
        self._raw = data

    def aggregate(self):
        """Fetch and aggregate raw job data from various sources concurrently based on the specified locations."""
        self._raw.clear()
        israel_locs = [loc for loc in self.locations if loc in config.normalized_cites_map]
        other_locs = [loc for loc in self.locations if loc not in config.normalized_cites_map]

        tasks = []

        if israel_locs:
            tasks.append(self._fetch_goonzile())

        if other_locs:
            tasks.append(self._fetch_adzuna())
            tasks.append(self._fetch_remotive())
            tasks.append(self._fetch_remoteok())

        if 'germany' in other_locs:
            tasks.append(self._fetch_arbeitnow())

        # Execute all fetch functions in parallel threads
        with ThreadPoolExecutor() as executor:
            executor.map(lambda f: f(), tasks)

    def filter_and_dedupe(self):
        """
        Filters raw job entries based on primary and secondary keywords and locations.
        Supports multi-word phrases with an optional word in between (e.g., 'cloud engineer' matches
        'cloud devops engineer', but not 'cloud, engineer').

        Returns:
            List[Dict]: A list of filtered and deduplicated job entries.
        """
        @staticmethod
        def phrase_with_optional_middle(phrase, text):
            """
            Check if the words in 'phrase' appear in order in 'text' with at most one word in between,
            and with no punctuation like comma or dot between.

            Parameters:
                phrase (str): Phrase to search (e.g., "cloud engineer")
                text (str): The text to search in

            Returns:
                bool: True if found as described, else False.
            """
            phrase = phrase.lower().strip()
            text = text.lower()
            text = re.sub(r'\s+', ' ', text)

            words = phrase.split()
            if len(words) != 2:
                return phrase in text  # fallback for single-word phrases

            word1, word2 = words
            pattern = r'\b' + re.escape(word1) + r'(?:\s+\w+)?\s+' + re.escape(word2) + r'\b'

            matches = re.finditer(pattern, text)
            for match in matches:
                between = match.group(0)
                if not re.search(r'[.,;:/\-]', between):
                    return True
            return False

        # If no secondary keywords provided, reuse primary keywords
        if not self.secondary_keywords or self.secondary_keywords == ['none']:
            self.secondary_keywords = self.keywords

        seen = set()
        results = []
        for job in self._raw:
            desc = job.get("Description", "").lower()
            loc = job.get("Location", "").lower()

            matched_keys = [
                k for k in self.keywords if phrase_with_optional_middle(k, desc)
            ]
            matched_secondary = [
                k for k in self.secondary_keywords if phrase_with_optional_middle(k, desc)
            ]
            matched_locs = [l for l in self.locations if l in loc]

            if matched_keys and matched_secondary and matched_locs:
                url = job.get("Link")
                if url and url not in seen:
                    seen.add(url)
                    results.append({
                        "Keyword": ", ".join(matched_keys),
                        "Secondary Keyword": ", ".join(matched_secondary),
                        "Description": job.get("Description", ""),
                        "Link": url,
                        "Location": job.get("Location", ""),
                        "Published At": job.get("Published At", ""),
                        "Full Description": job.get("Full Description", "")
                    })

        return results

    @staticmethod
    def sort_by_preference(jobs, sort_by, preferences):
        """
        Sorts job entries based on user-preferred field or by date.

        Args:
            jobs (List[Dict]): List of job entries.
            sort_by (str): The field to sort by ('location', 'keyword', or 'published at').
            preferences (List[str]): List of preferred values to prioritize (used only for location/keyword).

        Returns:
            List[Dict]: Sorted list of job entries.
        """

        if sort_by.lower() == "published at":
            def parse_date(date_str):
                try:
                    # Replace 'Z' with +00:00 to make it ISO format with timezone
                    date_str = date_str.replace("Z", "+00:00")
                    dt = datetime.fromisoformat(date_str)
                    # Ensure all dates are timezone-aware
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt
                except:
                    return datetime.min.replace(tzinfo=timezone.utc)

            return sorted(jobs, key=lambda job: parse_date(job.get("Published At", "")), reverse=True)

        else:
            def get_sort_index(job):
                field = job.get(sort_by.capitalize(), "").lower()
                for i, pref in enumerate(preferences):
                    if pref.lower() in field:
                        return i
                return len(preferences)

            return sorted(jobs, key=get_sort_index)

    # =============  PRIVATE HELPERS - FETCHERS =============

    def _fetch_remotive(self):
        """
         Fetch remote job listings from the Remotive API for each primary keyword.
        """
        url = "https://remotive.com/api/remote-jobs"
        for kw in self.keywords:
            resp = requests.get(url, params={"search": kw, "limit": self.limit})
            resp.raise_for_status()
            for job in resp.json().get("jobs", []):
                self._raw.append({
                    "Description": job.get("title", ""),
                    "Link": job.get("url", ""),
                    "Location": job.get("candidate_required_location", ""),
                    "Published At": job.get("date", ""),
                    "Full Description": job.get("description", "")
                })

    def _fetch_goonzile(self):
        """
         Fetch job listings from the Goonzile (Airtable) source, specifically for Israeli locations.
        """
        s = requests.Session()
        headers = config.GOONZILE_BASE_HEADERS
        url = config.GOONZILE_IFRAME_URL
        step = s.get(url, headers=headers)
        x = step.text

        start = config.GOONZILE_IFRAME_URL_START
        end = config.GOONZILE_IFRAME_URL_END
        new_url = ('https://airtable.com' + x[x.find(start) +
        len(start):x.rfind(end)].strip().replace('u002F','').replace('"','').replace(  '\\', '/')[:-1])

        start = 'var headers = '
        end = "headers['x-time-zone'] "
        dirty_auth_json = x[x.find(start) + len(start):x.rfind(end)].strip()[:-1]
        auth_json = json.loads(dirty_auth_json)

        new_headers = config.GOONZILE_BASE_HEADERS.copy()
        new_headers['X-Airtable-Application-Id'] = auth_json['x-airtable-application-id']
        new_headers['X-Airtable-Page-Load-Id'] = auth_json['x-airtable-page-load-id']

        json_data = s.get(new_url, headers=new_headers).json()
        cols = {x['id']: x['name'] for x in json_data['data']['table']['columns']}
        rows = json_data['data']['table']['rows']
        df = pd.json_normalize(rows)
        df.columns = [next((x.replace('cellValuesByColumnId.', '').replace(k, v) for k, v in cols.items() if k in x), x)
                      for x in df.columns]

        id_to_city = {}
        for city, ids in config.normalized_cites_map.items():
            for id in ids:
                id_to_city[id] = city

        if "Location" in df.columns:
            df = df[df["Location"].apply(lambda x: any(i in set(id_to_city.keys()) for i in x) if isinstance(x, list) else False)]

        desired_cols = ['Job Title', 'Position Link', 'Company', 'Location', 'createdTime', 'Job Description']
        existing_cols = [col for col in desired_cols if col in df.columns]
        output_df = df[existing_cols]

        if 'Location' in output_df.columns:
            output_df.loc[:, 'Location'] = output_df['Location'].apply(
                lambda ids: next((id_to_city[i] for i in ids if i in id_to_city), "Israel") if isinstance(ids,
                                                                                                list) else "Israel")

        for _, row in output_df.iterrows():
            # Safely extract the job description
            desc_raw = row.get('Job Description', '')
            if isinstance(desc_raw, list):
                # Airtable may return a list of dicts like [{'text': 'line 1'}, {'text': 'line 2'}]
                full_desc = " ".join(part.get('text', '') for part in desc_raw if isinstance(part, dict))
            else:
                full_desc = str(desc_raw)

            if not full_desc.strip():
                print(f"Empty description for: {row.get('Job Title', 'Unknown')} @ {row.get('Company', 'Unknown')}")

            # Append the job
            self._raw.append({
                "Description": f"{row['Job Title']} at {row.get('Company', '')}".strip(),
                "Link": row['Position Link'],
                "Location": row['Location'],
                "Published At": row['createdTime'],
                "Full Description": full_desc
            })

    def _fetch_adzuna(self):
        """
         Fetch job listings from the Adzuna API for each keyword-location combination.
        """
        for kw in self.keywords:
            for loc in self.locations:
                country_code = None
                if loc in country_map:
                    country_code = country_map[loc]
                else:
                    continue
                for page in range(1, 10):
                    base_url = config.ADZUNA_API_URL_TEMPLATE.format(country=country_code, page=page)
                    params = {
                        "app_id": config.ADZUNA_APP_ID,
                        "app_key": config.ADZUNA_APP_KEY,
                        "what": kw,
                        "where":  loc,
                        "results_per_page": 50,
                    }
                    try:
                        resp = requests.get(base_url, params=params)
                        resp.raise_for_status()
                        results = resp.json().get("results", [])
                        if not results:
                            break
                        for job in results:
                            self._raw.append({
                                "Description": job.get("title", ""),
                                "Link": job.get("redirect_url", ""),
                                "Location": job.get("location", {}).get("display_name", ""),
                                "Published At": job.get("created", ""),
                                "Full Description": job.get("description", "")
                            })
                    except Exception as e:
                        print(f"\u274c Adzuna failed: {e}")
                        break

    def _fetch_arbeitnow(self):
        """
        Fetch job listings from the Arbeitnow API.
        """
        for page in range(1, 10):
            url = "https://www.arbeitnow.com/api/job-board-api"
            try:
                resp = requests.get(url, params={"page": page})
                resp.raise_for_status()
                jobs = resp.json().get("data", [])
                if not jobs:
                    break
                for job in jobs:
                    self._raw.append({
                        "Description": job.get("title", ""),
                        "Link": job.get("url", ""),
                        "Location": job.get("location", ""),
                        "Published At": job.get("published_at", "")  # Assuming the field is named 'published_at'
                    })
            except Exception as e:
                print(f"Arbeitnow page {page} failed: {e}")
                break

    def _fetch_remoteok(self):
        """
        Fetch job listings from the RemoteOK API.
        """
        url = "https://remoteok.com/api"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()[1:]
        for item in data:
            self._raw.append({
                "Description": item.get("position", ""),
                "Link": item.get("url", ""),
                "Published At": item.get("date", ""),
                "Full Description": item.get("description", "")
            })









