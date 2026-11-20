import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3/"

def search_videos(query, max_results=10, live_only=False):
    """Search YouTube for videos matching a query."""

    if not API_KEY:
        raise RuntimeError("YOUTUBE_API_KEY is missing from .env")

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "order": "viewCount",
        "key": API_KEY
    }

    if live_only:
        params["eventType"] = "live"

    response = requests.get(
        f"{BASE_URL}search",
        params=params,
        timeout=20
    )
    response.raise_for_status()

    return response.json().get("items", [])


def fetch_video_details(video_ids):
    """Retrieve statistics and live-stream details for video IDs."""

    if not video_ids:
        return []

    params = {
        "part": "snippet,statistics,liveStreamingDetails",
        "id": ",".join(video_ids),
        "key": API_KEY
    }

    response = requests.get(
        f"{BASE_URL}videos",
        params=params,
        timeout=20
    )
    response.raise_for_status()

    return response.json().get("items", [])

def is_gta_vi_video(result):
    """Check whether a search result is specifically about GTA VI."""

    title = result.get("snippet", {}).get("title", "").lower()

    accepted_terms = [
        "grand theft auto vi",
        "grand theft auto 6",
        "gta vi",
        "gta 6"
    ]

    excluded_terms = [
        "grand theft auto v",
        "gta v",
        "gta 5"
    ]

    if any(term in title for term in excluded_terms):
        return False

    return any(term in title for term in accepted_terms)


def fetch_youtube_observations():
    """
    Collect GTA VI video statistics and publicly available
    concurrent viewer counts from active livestreams.
    """

    print("Searching for GTA VI videos...")
    video_results = search_videos(
        query="Grand Theft Auto VI",
        max_results=10
    )

    print("Searching for active GTA VI livestreams...")
    live_results = search_videos(
        query="GTA VI",
        max_results=10,
        live_only=True
    )

    # Combine results and remove duplicate video IDs.
    videos_by_id = {}


    for result in video_results + live_results:
        video_id = result.get("id", {}).get("videoId")

        if video_id and is_gta_vi_video(result):
            videos_by_id[video_id] = result        

    video_ids = list(videos_by_id.keys())

    print(f"Found {len(video_ids)} unique videos.")

    details = fetch_video_details(video_ids)

    observations = []
    collected_at = datetime.now(timezone.utc).isoformat()

    for video in details:
        video_id = video["id"]
        snippet = video.get("snippet", {})
        statistics = video.get("statistics", {})
        live_details = video.get("liveStreamingDetails", {})

        common_fields = {
            "source": "youtube",
            "video_id": video_id,
            "title": snippet.get("title"),
            "channel": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "collected_at": collected_at
        }

        # Video view count.
        if "viewCount" in statistics:
            observations.append({
                **common_fields,
                "metric": "video_views",
                "value": int(statistics["viewCount"]),
                "unit": "views"
            })

        # Like count may not be available for every video.
        if "likeCount" in statistics:
            observations.append({
                **common_fields,
                "metric": "video_likes",
                "value": int(statistics["likeCount"]),
                "unit": "likes"
            })

        # YouTube only exposes this value for eligible active streams.
        if "concurrentViewers" in live_details:
            observations.append({
                **common_fields,
                "metric": "live_concurrent_viewers",
                "value": int(live_details["concurrentViewers"]),
                "unit": "viewers"
            })

    return observations
