

import json

from pathlib import Path
from datetime import datetime, timezone

from sources.wikimedia.client import fetch_pageviews
from sources.youtube.client import fetch_youtube_observations


def main():
    print("=" * 50)
    print("GTA VI COMMUNITY MONITOR")
    print("=" * 50)

    # Wikimedia
    print("\n[1] WIKIMEDIA COLLECTOR")

    try:
        wikimedia_data = fetch_pageviews(days=30)

        print(f"Received {len(wikimedia_data)} observations.")

        latest = wikimedia_data[-1]
        print("\nLatest Wikipedia observation:")
        print(json.dumps(latest, indent=4))

        total_views = sum(item["views"] for item in wikimedia_data)
        print(f"Total Wikipedia pageviews: {total_views}")

    except Exception as error:
        print(f"Wikimedia collector failed: {error}")
        raise

    # YouTube
    print("\n[2] YOUTUBE COLLECTOR")

    try:
        youtube_data = fetch_youtube_observations()

        print(f"Received {len(youtube_data)} observations.")

        if youtube_data:
            print("\nSample YouTube observations:")
            print(json.dumps(youtube_data[:5], indent=4))

            live_count = sum(
                1 for item in youtube_data
                if item["metric"] == "live_concurrent_viewers"
            )

            print(f"\nLive viewer observations: {live_count}")
        else:
            print("No YouTube statistics were returned.")

    except Exception as error:
        print(f"YouTube collector failed: {error}")
        raise

    print("\n" + "=" * 50)
    print("COLLECTION COMPLETED")
    print("=" * 50)

    

    # Save observations for the processor
    output_directory = Path(__file__).resolve().parent.parent / "processor" / "input"
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "observations.json"

    collected_data = {
        "project": "GTA VI Community Monitor",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "observations": wikimedia_data + youtube_data
    }

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(collected_data, file, indent=4, ensure_ascii=False)

    print(f"\nSaved {len(collected_data['observations'])} observations.")
    print(f"Output file: {output_file}")

if __name__ == "__main__":
    main()
