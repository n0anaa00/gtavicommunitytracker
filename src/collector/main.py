
from sources.wikimedia.client import fetch_pageviews
import json


def main():
    print("Starting GTA VI Community Monitor")
    print("Fetching Wikimedia pageview data...")

    try:
        observations = fetch_pageviews(days=30)

        print(f"Received {len(observations)} observations.")

        latest = observations[-1]

        print("\nLatest available observation:")
        print(json.dumps(latest, indent=4))

        total_views = sum(
            observation["views"]
            for observation in observations
        )

        print(f"\nTotal views in period: {total_views}")

    except Exception as error:
        print(f"Wikimedia collector failed: {error}")
        raise


if __name__ == "__main__":
    main()
