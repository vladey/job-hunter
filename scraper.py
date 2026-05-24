import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()


def search_jobs():

    api_key = os.getenv("SERPAPI_KEY")

    positions = [
        "Plant Manager",
        "Operations Manager",
        "Factory Director",
        "Production Director",
        "General Manager",
        "COO",
        "Production Manager",
        "Site Director",
        "Site Manager"
    ]

    locations = [
        "Plovdiv Bulgaria",
        "Sofia Bulgaria"
    ]

    jobs = []

    if not api_key:
        print("ERROR: SERPAPI_KEY missing")
        return []

    for position in positions:

        for location in locations:

            query = f"{position} {location}"

            print("Searching:", query)

            params = {
                "engine": "google_jobs",
                "q": query,
                "api_key": api_key
            }

            try:

                search = GoogleSearch(params)

                results = search.get_dict()

                job_results = results.get("jobs_results", [])

                print("RESULTS:", len(job_results))

                for item in job_results:

                    title = item.get("title", "")

                    company = item.get("company_name", "")

                    city = item.get("location", "")

                    description = item.get("description", "")

                    link = item.get("share_link", "")

                    if link:

                        jobs.append({
                            "title": f"{title} - {company}",
                            "city": city,
                            "link": link,
                            "snippet": description
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
