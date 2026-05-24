from playwright.sync_api import sync_playwright


def search_jobs():

    urls = [
        "https://www.zaplata.bg/search/?q=Plant+Manager",
        "https://www.zaplata.bg/search/?q=Operations+Manager",
        "https://www.zaplata.bg/search/?q=Production+Manager",
        "https://www.zaplata.bg/search/?q=Site+Manager",
        "https://www.zaplata.bg/search/?q=Factory+Director",
        "https://www.zaplata.bg/search/?q=Production+Director",
        "https://www.zaplata.bg/search/?q=General+Manager",
        "https://www.zaplata.bg/search/?q=COO",
    ]

    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in urls:
            print("Opening:", url)

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(5000)

                links = page.locator("a").all()
                print("Links found:", len(links))

                for link in links:
                    href = link.get_attribute("href")
                    text = link.inner_text().strip()

                    if not href:
                        continue

                    if href.startswith("/"):
                        href = "https://www.zaplata.bg" + href

                    if "/rabota/" not in href and "/obiava/" not in href:
                        continue

                    title = text if text else "Обява от Zaplata.bg"

                    jobs.append({
                        "title": title[:120],
                        "city": "Пловдив/София",
                        "link": href,
                        "snippet": url
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
