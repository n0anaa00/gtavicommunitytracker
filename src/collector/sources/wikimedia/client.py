
import requests
from datetime import datetime, timedelta, timezone
from urllib.parse import quote


BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews"

PROJECT = "en.wikipedia.org"
ARTICLE = "Grand_Theft_Auto_VI"

HEADERS = {
    "User-Agent": "GTACommunityMonitor/1.0 (course project)"
}


def fetch_pageviews(days=30):
    """
    Fetch daily Wikipedia pageviews for the GTA VI article.

    The API can have a reporting delay, so the requested
    period ends two days before the current UTC date.
    """

    today = datetime.now(timezone.utc).date()

    end_date = today - timedelta(days=2)
    start_date = end_date - timedelta(days=days - 1)

    start = start_date.strftime("%Y%m%d")
    end = end_date.strftime("%Y%m%d")

    article = quote(ARTICLE, safe="")

    url = (
        f"{BASE_URL}/per-article/"
        f"{PROJECT}/all-access/all-agents/"
        f"{article}/daily/{start}/{end}"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    result = response.json()

    items = result.get("items", [])

    if not items:
        raise ValueError("Wikimedia returned no pageview data.")

    observations = []

    for item in items:
        observation = {
            "source": "wikimedia",
            "metric": "pageviews",
            "article": ARTICLE,
            "date": item["timestamp"][:8],
            "views": int(item["views"]),
            "granularity": "daily"
        }

        observations.append(observation)

    return observations
