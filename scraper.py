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
        "Site Manager",
    ]

    locations = ["Plovdiv, Bulgaria", "Sofia, Bulgaria"]

    jobs = []

    if not api_key:
        print("ERROR: SERPAPI_KEY is missing")
        return jobs

    for position in positions:
        for location in locations:
            query = f"{position} {location}"

            print("Searching Google Jobs:", query)

            params = {
                "engine": "google_jobs",
                "q": query,
                "api_key": api_key,
                "hl": "en",
                "gl": "bg",
            }

            try:
                search = GoogleSearch(params)
                results = search.get_dict()

                if "error" in results:
                    print("SERPAPI ERROR:", results["error"])
                    continue

                job_results = results.get("jobs_results", [])
                print("JOBS RESULTS FOUND:", len(job_results))

                for item in job_results:
                    title = item.get("title", "")
                    company = item.get("company_name", "")
                    job_location = item.get("location", location)
                    via = item.get("via", "")
                    description = item.get("description", "")
                    share_link = item.get("share_link", "")

                    apply_link = share_link

                    apply_options = item.get("apply_options", [])
                    if apply_options:
                        apply_link = apply_options[0].get("link", share_link)

                    if apply_link:
                        jobs.append({
                            "title": f"{title} — {company}",
                            "city": job_location,
                            "link": apply_link,
                            "source": via,
                            "snippet": description[:300],
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

    return unique_jobs[:20]            params = {
                "engine": "google",
                "q": query,
                "api_key": api_key,
                "num": 10,
                "hl": "bg",
                "gl": "bg"
            }

            try:
                search = GoogleSearch(params)
                results = search.get_dict()

                organic = results.get("organic_results", [])
                print("RESULTS FOUND:", len(organic))

                for result in organic:
                    title = result.get("title", "")
                    link = result.get("link", "")
                    snippet = result.get("snippet", "")

                    allowed_sites = [
                        "jobs.bg",
                        "zaplata.bg",
                        "jobtiger.bg",
                        "rabota.bg",
                        "linkedin.com",
                        "karieri.bg",
                        "indeed.com"
                    ]

                    if link and any(site in link for site in allowed_sites):
                        jobs.append({
                            "title": title,
                            "city": city,
                            "link": link,
                            "source": link,
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
