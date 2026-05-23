def search_jobs_bg():
    return []


def search_zaplata_bg():
    return []


def search_jobtiger_bg():
    return []


def search_linkedin():
    return []


def search_jobs():
    jobs = []

    jobs += search_jobs_bg()
    jobs += search_zaplata_bg()
    jobs += search_jobtiger_bg()
    jobs += search_linkedin()

    unique = []
    seen = set()

    for job in jobs:
        if job["link"] not in seen:
            seen.add(job["link"])
            unique.append(job)

    return unique[:20]
    for job in jobs:

        if job["link"] not in seen:

            seen.add(job["link"])

            unique_jobs.append(job)

    return unique_jobs[:10]
