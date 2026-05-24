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
        "Site Manager Plovdiv"
    ]

    sites = [
        "jobs.bg",
        "zaplata.bg",
        "jobtiger.bg",
        "linkedin.com/jobs"
    ]

    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        for site in sites:

            for query in queries:

                url = f"https://www.google.com/search?q=site:{site}+{query.replace(' ', '+')}"

                print("Opening:", url)

                try:

                    page.goto(url, timeout=30000)

                    page.wait_for_timeout(3000)

                    links = page.locator("a").all()

                    for link in links:

                        href = link.get_attribute("href")

                        text = link.inner_text()

                        if not href:
                            continue

                        if site not in href:
                            continue

                        jobs.append({
                            "title": text[:100],
                            "city": query,
                            "link": href,
                            "snippet": site
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
