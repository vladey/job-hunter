import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def search_jobs():
    positions = [
        "Plant Manager",
        "Operations Manager",
        "Production Manager",
        "Site Manager",
        "Site Director"
    ]

    cities = ["Пловдив", "София"]
    jobs = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for position in positions:
        url = f"https://www.jobs.bg/front_job_search.php?keywords={quote(position)}"

        print("Checking:", url)

        try:
            response = requests.get(url, headers=headers, timeout=20)

            print("Status code:", response.status_code)
            print("Page length:", len(response.text))

            soup = BeautifulSoup(response.text, "html.parser")

            page_text = soup.get_text(" ", strip=True)

            for city in cities:
                if city in page_text:
                    jobs.append({
                        "title": f"{position} - намерен текст за {city}",
                        "city": city,
                        "link": url
                    })

        except Exception as e:
            print("ERROR:", e)

    print("Jobs found:", len(jobs))

    return jobs
