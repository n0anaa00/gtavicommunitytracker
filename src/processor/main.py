
import json
from pathlib import Path
from datetime import datetime, timezone

from normalizer import normalize_observations, build_summary


def main():
    print("=" * 50)
    print("GTA VI COMMUNITY PROCESSOR")
    print("=" * 50)

    processor_directory = Path(__file__).resolve().parent
    input_file = processor_directory / "input" / "observations.json"

    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_file}. "
            "Run the collector first."
        )

    print("\n[1] Loading collected observations...")

    with input_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    observations = data.get("observations", [])

    print(f"Loaded {len(observations)} observations.")

    print("\n[2] Validating and normalizing...")

    normalized, rejected = normalize_observations(observations)

    print(f"Accepted: {len(normalized)}")
    print(f"Rejected: {len(rejected)}")

    print("\n[3] Aggregating metrics...")

    summary = build_summary(normalized)

    print("\nMetric summary:")

    for source, metrics in summary.items():
        print(f"\n{source.upper()}")

        for metric, values in metrics.items():
            print(
                f"  {metric}: "
                f"{values['total']} {values['unit']} "
                f"({values['count']} observations)"
            )

    print("\n[4] Saving processor output...")

    output_file = (
        processor_directory / "normalized_observations.json"
    )

    summary_file = processor_directory / "summary.json"

    output_data = {
        "project": "GTA VI Community Monitor",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "observation_count": len(normalized),
        "observations": normalized,
        "rejected_observations": rejected
    }

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=4, ensure_ascii=False)

    with summary_file.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)

    print(f"Normalized data: {output_file}")
    print(f"Metric summary: {summary_file}")

    print("\n" + "=" * 50)
    print("PROCESSING COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    main()
