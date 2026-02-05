import json
from pathlib import Path

LOG_FILE = Path("logs.txt")
OUTPUT_CLEANED_LOGS = Path("clean_logs.txt")
OUTPUT_SUMMARY_JSON = Path("summary.json")

ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}

def parse_line(line: str):
    line = line.strip()
    if not line:
        return None
    parts = [part.strip() for part in line.split('|')]
    if len(parts) != 4:
        return None
    return tuple(parts)

def normalize_level(level: str) -> str:
    return level.upper()

def main():
    total_lines = 0
    valid_lines = 0
    invalid_lines = 0
    levels = {"INFO": 0, "WARN": 0, "ERROR": 0, "INVALID_LEVEL": 0}
    services_count = {}
    error_messages_count = {}

    if not LOG_FILE.exists():
        print(f"ERROR: Could not find {LOG_FILE}. Make sure logs.txt is in the same folder.")
        return

    with open(LOG_FILE, 'r') as file, open(OUTPUT_CLEANED_LOGS, 'w') as clean_file:
        for line in file:
            total_lines += 1
            parsed = parse_line(line)
            if parsed is None:
                invalid_lines += 1
                continue

            timestamp, level, service, message = parsed
            normalized_level = normalize_level(level)

            if normalized_level in ALLOWED_LEVELS:
                valid_lines += 1
                levels[normalized_level] += 1

                # Count services
                services_count[service] = services_count.get(service, 0) + 1

                # Count error messages for ERROR level
                if normalized_level == "ERROR":
                    error_messages_count[message] = error_messages_count.get(message, 0) + 1

                # Write the valid log to the clean logs file
                clean_file.write(f"{timestamp} | {normalized_level} | {service} | {message}\n")
            else:
                levels["INVALID_LEVEL"] += 1
                invalid_lines += 1

    # Generate top services and top error messages
    top_services = sorted(services_count.items(), key=lambda x: x[1], reverse=True)[:3]
    top_errors = sorted(error_messages_count.items(), key=lambda x: x[1], reverse=True)[:3]

    # Create summary dictionary
    summary = {
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "invalid_lines": invalid_lines,
        "levels": levels,
        "top_services": [{"service": service, "count": count} for service, count in top_services],
        "top_errors": [{"message": message, "count": count} for message, count in top_errors],
    }

    # Write the summary to a JSON file
    with open(OUTPUT_SUMMARY_JSON, 'w') as json_file:
        json.dump(summary, json_file, indent=4)

    print(f"Summary saved to {OUTPUT_SUMMARY_JSON}")
    print(f"Clean logs saved to {OUTPUT_CLEANED_LOGS}")

if __name__ == "__main__":
    main()
