import imaplib
import email
import os
import re
from bs4 import BeautifulSoup
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()


def decode_subject(msg):
    subject = msg.get("Subject", "")
    decoded_parts = decode_header(subject)
    result = ""

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            result += part.decode(encoding or "utf-8", errors="ignore")
        else:
            result += part

    return result


def get_body(msg):
    html_body = ""
    text_body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()

            if content_type not in ["text/html", "text/plain"]:
                continue

            payload = part.get_payload(decode=True)

            if not payload:
                continue

            decoded = payload.decode(errors="ignore")

            if content_type == "text/html":
                html_body += decoded
            else:
                text_body += decoded
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            text_body = payload.decode(errors="ignore")

    return html_body, text_body


def get_job_emails():
    user = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_APP_PASSWORD")

    keywords = [
        "plant manager",
        "operations manager",
        "production manager",
        "factory director",
        "production director",
        "general manager",
        "site manager",
        "site director",
        "coo",
        "директор",
        "мениджър",
        "ръководител",
        "производство",
        "операции",
        "завод"
    ]

    good_domains = [
        "jobs.bg",
        "linkedin.com",
        "zaplata.bg",
        "jobtiger.bg",
    ]

    bad_words = [
        "unsubscribe",
        "preferences",
        "help",
        "support",
        "privacy",
        "terms",
        "notification",
        "premium",
        "learning",
        "advice",
        "article",
        "salary-guide",
        "settings",
        "login",
        "signin",
        "share",
    ]

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(user, password)
    imap.select("INBOX")

    status, messages = imap.search(None, "ALL")
    email_ids = messages[0].split()

    results = []

    for mail_id in email_ids[-80:]:
        _, msg_data = imap.fetch(mail_id, "(RFC822)")

        for response_part in msg_data:
            if not isinstance(response_part, tuple):
                continue

            msg = email.message_from_bytes(response_part[1])
            subject = decode_subject(msg)
            sender = msg.get("From", "")

            combined_header = f"{subject} {sender}".lower()

            if not (
                "linkedin" in combined_header
                or "jobs.bg" in combined_header
                or "zaplata" in combined_header
                or "jobtiger" in combined_header
            ):
                continue

            html_body, text_body = get_body(msg)
            found_links = []

            if html_body:
                soup = BeautifulSoup(html_body, "html.parser")

                for a in soup.find_all("a"):
                    href = a.get("href")
                    text = a.get_text(" ", strip=True)

                    if not href:
                        continue

                    combined = f"{subject} {text} {href}".lower()

                    if any(k in combined for k in keywords):
                        found_links.append({
                            "title": text or subject,
                            "link": href,
                            "source": sender,
                            "snippet": subject
                        })

            urls = re.findall(r"https?://[^\s<>\"']+", text_body)

            for url in urls:
                combined = f"{subject} {url}".lower()

                if any(k in combined for k in keywords):
                    found_links.append({
                        "title": subject,
                        "link": url,
                        "source": sender,
                        "snippet": subject
                    })

            for item in found_links:
                results.append({
                    "title": item["title"][:120],
                    "city": "Пловдив/София",
                    "link": item["link"],
                    "source": item["source"],
                    "snippet": item["snippet"]
                })

    imap.logout()

    unique = []
    seen = set()

    for job in results:
        link = job["link"]

        if link in seen:
            continue

        seen.add(link)
        unique.append(job)

    print("JOB LINKS FOUND:", len(unique))

    filtered = []

    for job in unique:
        link_l = job["link"].lower()
        title_l = job["title"].lower()

        if not any(domain in link_l for domain in good_domains):
            continue

        if any(word in link_l for word in bad_words):
            continue

        if any(word in title_l for word in bad_words):
            continue

        filtered.append(job)

    print("FILTERED JOBS:", len(filtered))

    return filtered[:15]
