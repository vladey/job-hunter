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

    cities = ["Пловдив", "София", "Plovdiv", "Sofia"]

    sites = [
        "jobs.bg",
        "zaplata.bg",
        "jobtiger.bg",
        "rabota.bg",
        "linkedin.com/jobs"
    ]

    jobs = []

    for site in sites:
        for position in positions:
            for city in cities:
                query = f'site:{site} "{position}" "{city}" job OR работа'

                print("Searching:", query)

                params = {
                    "engine": "google",
                    "q": query,
                    "api_key": api_key,
                    "num": 5,
                    "hl": "bg",
                    "gl": "bg"
                }

                try:
                    search = GoogleSearch(params)
                    results = search.get_dict()

                    for result in results.get("organic_results", []):
                        title = result.get("title", "")
                        link = result.get("link", "")
                        snippet = result.get("snippet", "")

                        if link:
                            jobs.append({
                                "title": title,
                                "city": city,
                                "link": link,
                                "source": site,
                                "snippet": snippet
                            })

                except Exception as e:
                    print("ERROR:", e)

    unique = []
    seen = set()

    for job in jobs:
        if job["link"] not in seen:
            seen.add(job["link"])
            unique.append(job)

    print("Jobs found:", len(unique))

    return unique[:20]
