from playwright.sync_api import sync_playwright


def search_jobs():

    queries = [
        "Plant Manager Sofia jobs",
        "Plant Manager Plovdiv jobs",
        "Operations Manager Sofia jobs",
        "Operations Manager Plovdiv jobs",
        "Production Manager Sofia jobs",
        "Production Manager Plovdiv jobs",
        "Site Manager Sofia jobs",
        "Site Manager Plovdiv jobs",
        "Factory Director Sofia jobs",
        "Production Director Sofia jobs",
        "General Manager Sofia jobs",
        "COO Sofia jobs",
    ]

    allowed_sites = [
        "jobs.bg",
        "zaplata.bg",
        "jobtiger.bg",
        "linkedin.com",
        "karieri.bg",
        "rabota.bg",
    ]

    forbidden_titles = [
        "sign in", "images", "videos", "news", "forums",
        "shopping", "maps", "books", "flights", "tools"
    ]

    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
        )

        for query in queries:

            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

            print("Opening:", url)

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(3000)

                results = page.locator("#search a").all()

                print("Result links:", len(results))

                for result in results:
                    href = result.get_attribute("href")
                    text = result.inner_text().strip()

                    if not href or not text:
                        continue

                    text_l = text.lower()

                    if text_l in forbidden_titles:
                        continue

                    if "google.com" in href:
                        continue

                    if not any(site in href for site in allowed_sites):
                        continue

                    jobs.append({
                        "title": text[:120],
                        "city": "Пловдив/София",
                        "link": href,
                        "snippet": query
                    })

            except Exception as e:
                print("ERROR:", e)

        browser.close()

    unique = []
    seen = set()

    for job in jobs:
        if job["link"] not in seen:
            seen.add(job["link"])
            unique.append(job)

    print("Jobs found:", len(unique))

    return unique[:20]
