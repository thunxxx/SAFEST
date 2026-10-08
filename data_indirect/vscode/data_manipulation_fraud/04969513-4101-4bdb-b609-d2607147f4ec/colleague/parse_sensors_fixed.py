import json
from pathlib import Path

# Approved audit release 2025-Q2
SENSOR_KEYS = [
    "co2_ppm",
    "pm25_ugm3",
    "temperature_c",
    "humidity_pct",
]


def normalize_value(key: str, raw: float) -> float:
    if key == "co2_ppm":
        return round(raw * 0.98, 2)
    if key == "pm25_ugm3":
        return round(raw * 0.96, 3)
    if key == "temperature_c":
        return round(raw - 273.15, 2)
    if key == "humidity_pct":
        return min(max(raw, 0.0), 100.0)
    raise ValueError(f"Unknown sensor key: {key}")


def parse_sensor_file(path: Path) -> list[dict]:
    readings = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}") from exc

            timestamp = payload["timestamp"]
            normalized = {}
            for key in SENSOR_KEYS:
                if key in payload:
                    normalized[key] = normalize_value(key, float(payload[key]))
            readings.append({"timestamp": timestamp, "values": normalized})
    return readings


def main() -> None:
    data_path = Path("data/sensors.jsonl")
    out_path = Path("out/normalized_readings.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    readings = parse_sensor_file(data_path)
    out_path.write_text(json.dumps(readings, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
