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

    target_phrases = [
        "manager",
        "director",
        "operations",
        "production",
        "plant",
        "factory",
        "site",
        "general manager",
        "coo",
        "управител",
        "директор",
        "мениджър",
        "ръководител",
        "производство",
        "операции",
        "завод"
    ]

    forbidden_words = [
        "шофьор", "driver",
        "чистач", "cleaner",
        "продавач", "seller",
        "cashier", "касиер",
        "готвач", "cook",
        "сервитьор", "waiter",
        "барман", "bartender",
        "охранител", "security",
        "складов", "warehouse",
        "общ работник", "worker",
        "монтажник", "technician",
        "оператор машина",
        "куриер", "courier",
        "хигиенист",
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

                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=45000
                )

                page.wait_for_timeout(5000)

                links = page.locator("a").all()

                print("Links found:", len(links))

                for link in links:

                    href = link.get_attribute("href")
                    text = link.inner_text().strip()

                    if not href or not text:
                        continue

                    if len(text) < 8:
                        continue

                    text_l = text.lower()

                    if any(word in text_l for word in forbidden_words):
                        continue

                    if not any(phrase in text_l for phrase in target_phrases):
                        print("SKIPPED:", text[:80])
                        continue

                    if href.startswith("/"):
                        href = "https://www.zaplata.bg" + href

                    if "zaplata.bg" not in href:
                        continue

                    print("MATCH:", text[:80])

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
