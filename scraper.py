from playwright.sync_api import sync_playwright


def search_jobs():

    urls = [
        "https://www.zaplata.bg/search/?q=Plant+Manager",
        "https://www.zaplata.bg/search/?q=Operations+Manager",
        "https://www.zaplata.bg/search/?q=Production+Manager",
        "https://www.zaplata.bg/search/?q=Site+Manager",

        "https://www.jobtiger.bg/obiavi-za-rabota/?q=Plant%20Manager",
        "https://www.jobtiger.bg/obiavi-za-rabota/?q=Operations%20Manager",
        "https://www.jobtiger.bg/obiavi-za-rabota/?q=Production%20Manager",
        "https://www.jobtiger.bg/obiavi-za-rabota/?q=Site%20Manager",
    ]

    keywords = [
        "Plant Manager",
        "Operations Manager",
        "Production Manager",
        "Site Manager",
        "Factory Director",
        "Production Director",
        "General Manager",
        "COO"
    ]

    cities = [
        "София",
        "Пловдив",
        "Sofia",
        "Plovdiv"
    ]

    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
        )

        for url in urls:

            print("Opening:", url)

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(4000)

                links = page.locator("a").all()

                for link in links:
                    href = link.get_attribute("href")
                    text = link.inner_text().strip()

                    if not href or not text:
                        continue

                    text_l = text.lower()

                    keyword_match = any(k.lower() in text_l for k in keywords)
                    city_match = any(c.lower() in text_l for c in cities)

                    if not keyword_match:
                        continue

                    if not city_match:
                        continue

                    if href.startswith("/"):
                        if "zaplata.bg" in url:
                            href = "https://www.zaplata.bg" + href
                        elif "jobtiger.bg" in url:
                            href = "https://www.jobtiger.bg" + href

                    jobs.append({
                        "title": text[:120],
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
