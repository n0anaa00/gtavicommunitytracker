
from datetime import datetime, timezone


def normalize_observation(observation):
    """
    Convert source-specific observations into a common structure.
    """

    source = observation.get("source")
    metric = observation.get("metric")
    value = observation.get("value")

    # Wikimedia currently uses "views" rather than "value".
    if source == "wikimedia" and metric == "pageviews":
        value = observation.get("views")

    if source not in ("wikimedia", "youtube"):
        raise ValueError(f"Unsupported source: {source}")

    if not metric:
        raise ValueError("Observation is missing its metric.")

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Invalid metric value: {value}")

    if value < 0:
        raise ValueError(f"Negative metric value: {value}")

    # Wikimedia observations represent a daily reporting period.
    if source == "wikimedia":
        observed_at = observation.get("date")

        if not observed_at:
            raise ValueError("Wikimedia observation is missing its date.")

        observed_at = (
            datetime.strptime(observed_at, "%Y%m%d")
            .replace(tzinfo=timezone.utc)
            .isoformat()
        )

        unit = "pageviews"

    else:
        observed_at = observation.get("collected_at")

        if not observed_at:
            raise ValueError("YouTube observation is missing collected_at.")

        unit = observation.get("unit", "unknown")

    normalized = {
        "source": source,
        "metric": metric,
        "value": value,
        "unit": unit,
        "observed_at": observed_at
    }

    # Preserve relevant source-specific metadata.
    if source == "wikimedia":
        normalized["article"] = observation.get("article")

    if source == "youtube":
        normalized["video_id"] = observation.get("video_id")
        normalized["title"] = observation.get("title")
        normalized["channel"] = observation.get("channel")
        normalized["url"] = observation.get("url")
        normalized["published_at"] = observation.get("published_at")

    return normalized


def normalize_observations(observations):
    """
    Normalize a collection of observations.
    Invalid records are reported and skipped.
    """

    normalized = []
    rejected = []

    for index, observation in enumerate(observations):
        try:
            normalized.append(
                normalize_observation(observation)
            )

        except (ValueError, TypeError, KeyError) as error:
            rejected.append({
                "index": index,
                "reason": str(error)
            })

    return normalized, rejected


def build_summary(observations):
    """
    Produce basic source and metric summaries.

    These totals are metric-specific and should not be
    interpreted as unique people or unique audience reach.
    """

    summary = {}

    for observation in observations:
        source = observation["source"]
        metric = observation["metric"]
        value = observation["value"]

        if source not in summary:
            summary[source] = {}

        if metric not in summary[source]:
            summary[source][metric] = {
                "count": 0,
                "total": 0,
                "unit": observation["unit"]
            }

        summary[source][metric]["count"] += 1
        summary[source][metric]["total"] += value

    return summary
