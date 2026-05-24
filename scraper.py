from playwright.sync_api import sync_playwright


def search_jobs():

    queries = [
        "Plant Manager Sofia jobs.bg",
        "Plant Manager Plovdiv jobs.bg",
        "Operations Manager Sofia jobs.bg",
        "Operations Manager Plovdiv jobs.bg",
        "Production Manager Sofia jobs.bg",
        "Production Manager Plovdiv jobs.bg",
        "Site Manager Sofia jobs.bg",
        "Site Manager Plovdiv jobs.bg",
        "Plant Manager Sofia zaplata.bg",
        "Operations Manager Sofia zaplata.bg",
        "Production Manager Sofia zaplata.bg",
        "Plant Manager Sofia jobtiger.bg",
        "Operations Manager Sofia jobtiger.bg",
        "Production Manager Sofia jobtiger.bg",
        "Plant Manager Sofia linkedin jobs",
        "Operations Manager Sofia linkedin jobs",
        "Production Manager Sofia linkedin jobs"
    ]

    allowed_sites = [
        "jobs.bg",
        "zaplata.bg",
        "jobtiger.bg",
        "linkedin.com/jobs"
    ]

    bad_words = [
        "Sign in", "Images", "Videos", "News", "Forums",
        "Shopping", "Short videos", "Maps", "Books", "Flights",
        "All", "Search", "Tools"
    ]

    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        for query in queries:

            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

            print("Opening:", url)

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)

                links = page.locator("a").all()

                for link in links:

                    href = link.get_attribute("href")
                    text = link.inner_text().strip()

                    if not href or not text:
                        continue

                    if text in bad_words:
                        continue

                    if href.startswith("/"):
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
