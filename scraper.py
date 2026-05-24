import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()


def search_jobs():
    api_key = os.getenv("SERPAPI_KEY")

    queries = [
        'Plant Manager Sofia jobs.bg',
        'Plant Manager Plovdiv jobs.bg',
        'Operations Manager Sofia jobs.bg',
        'Operations Manager Plovdiv jobs.bg',
        'Production Manager Sofia jobs.bg',
        'Production Manager Plovdiv jobs.bg',
        'Site Manager Sofia jobs.bg',
        'Site Manager Plovdiv jobs.bg',
        'Factory Director Sofia jobs.bg',
        'General Manager Sofia jobs.bg',

        'Plant Manager Sofia zaplata.bg',
        'Plant Manager Plovdiv zaplata.bg',
        'Operations Manager Sofia zaplata.bg',
        'Operations Manager Plovdiv zaplata.bg',
        'Production Manager Sofia zaplata.bg',
        'Production Manager Plovdiv zaplata.bg',
        'Site Manager Sofia zaplata.bg',
        'Site Manager Plovdiv zaplata.bg',

        'Plant Manager Sofia LinkedIn jobs',
        'Operations Manager Sofia LinkedIn jobs',
        'Production Manager Sofia LinkedIn jobs',
        'Site Manager Sofia LinkedIn jobs',
        'Factory Director Sofia LinkedIn jobs',

        'Plant Manager Bulgaria jobs',
        'Operations Manager Bulgaria jobs',
        'Production Manager Bulgaria jobs',
        'Site Manager Bulgaria jobs'
    ]

    allowed_sites = [
        "jobs.bg",
        "zaplata.bg",
        "jobtiger.bg",
        "rabota.bg",
        "linkedin.com",
        "karieri.bg"
    ]

    jobs = []

    if not api_key:
        print("ERROR: SERPAPI_KEY missing")
        return []

    for query in queries:
        print("Searching:", query)

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "num": 10,
            "hl": "en",
            "gl": "bg"
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()

            if "error" in results:
                print("SERPAPI ERROR:", results["error"])
                continue

            organic = results.get("organic_results", [])
            print("RESULTS:", len(organic))

            for item in organic:
                title = item.get("title", "")
                link = item.get("link", "")
                snippet = item.get("snippet", "")

                if link and any(site in link for site in allowed_sites):
                    jobs.append({
                        "title": title,
                        "city": "Пловдив/София",
                        "link": link,
                        "snippet": snippet
                    })

        except Exception as e:
            print("ERROR:", e)

    unique_jobs = []
    seen = set()

    for job in jobs:
        if job["link"] not in seen:
            seen.add(job["link"])
            unique_jobs.append(job)

    print("Jobs found:", len(unique_jobs))

    return unique_jobs[:20]
