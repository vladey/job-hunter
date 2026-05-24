from playwright.sync_api import sync_playwright


def search_jobs():
    queries = [
        "Plant Manager Sofia",
        "Plant Manager Plovdiv",
        "Operations Manager Sofia",
        "Operations Manager Plovdiv",
        "Production Manager Sofia",
        "Production Manager Plovdiv",
        "Site Manager Sofia",
        "Site Manager Plovdiv",
        "Factory Director Sofia",
        "Production Director Sofia",
        "General Manager Sofia",
        "COO Sofia",
    ]

    sites = [
        "jobs.bg",
        "zaplata.bg",
        "jobtiger.bg",
        "rabota.bg",
        "linkedin.com/jobs",
    ]

    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
        )

        for site in sites:
            for query in queries:
                search_url = f"https://www.google.com/search?q=site:{site}+{query.replace(' ', '+')}"

                print("Opening:", search_url)

                try:
                    page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(2000)

                    links = page.locator("a").all()

                    for link in links:
                        href = link.get_attribute("href")
                        text = link.inner_text().strip()

                        if not href or not text:
                            continue

                        if site not in href:
                            continue

                        if "google" in href:
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
