import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def search_jobs():

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

    cities = ["Пловдив", "София"]

    jobs = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for position in positions:

        search = quote(position)

        url = f"https://www.jobs.bg/front_job_search.php?keywords={search}"

        try:

            response = requests.get(url, headers=headers, timeout=20)

            soup = BeautifulSoup(response.text, "html.parser")

            links = soup.find_all("a")

            for link in links:

                text = link.get_text(strip=True)

                href = link.get("href")

                if href and text:

                    for city in cities:

                        if city.lower() in text.lower():

                            jobs.append({
                                "title": text,
                                "city": city,
                                "link": href
                            })

        except Exception as e:
            print(e)

    unique_jobs = []

    seen = set()

    for job in jobs:

        if job["link"] not in seen:

            seen.add(job["link"])

            unique_jobs.append(job)

    return unique_jobs[:10]
