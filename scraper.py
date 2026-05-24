from playwright.sync_api import sync_playwright


def search_jobs():

    urls = [
        "https://www.zaplata.bg/search/?q=Plant+Manager",
    ]

    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in urls:
            print("Opening:", url)

            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(5000)

            links = page.locator("a").all()
            print("Links found:", len(links))

            count = 0

            for link in links:
                href = link.get_attribute("href")
                text = link.inner_text().strip()

                if not href:
                    continue

                print("HREF:", href)
                print("TEXT:", text[:100])
                print("---")

                count += 1

                if count >= 50:
                    break

        browser.close()

    print("Jobs found:", len(jobs))

    return jobs
