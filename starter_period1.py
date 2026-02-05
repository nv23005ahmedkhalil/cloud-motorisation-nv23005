from pathlib import Path

LOG_FILE = Path("logs.txt")
OUTPUT_REPORT = Path("period1_report.txt")

ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}

def parse_line(line: str):
    """
    Parse a single log line.
    Returns a tuple: (timestamp, level, service, message) OR None if format is invalid.

    Expected format:
    timestamp | level | service | message
    """
    # TODO 1: Strip whitespace and ignore empty lines
    line = line.strip()
    if not line:
        return None  # Ignore empty lines

    # TODO 2: Split by '|' and trim whitespace around each part
    parts = [part.strip() for part in line.split('|')]

    # TODO 3: If not exactly 4 parts, return None
    if len(parts) != 4:
        return None

    # TODO 4: Return the parts (timestamp, level, service, message)
    return tuple(parts)

def normalize_level(level: str) -> str:
    """Normalize log level to uppercase."""
    # TODO 5: Return the level in uppercase
    return level.upper()

def main():
    # Counters
    total_lines = 0
    invalid_lines = 0
    level_counts = {
        "INFO": 0,
        "WARN": 0,
        "ERROR": 0,
        "INVALID_LEVEL": 0,
    }

    # Safety check
    if not LOG_FILE.exists():
        print(f"ERROR: Could not find {LOG_FILE}. Make sure logs.txt is in the same folder.")
        return

    # TODO 6: Open logs.txt and loop through each line
    with open(LOG_FILE, 'r') as file:
        for line in file:
            total_lines += 1
            parsed = parse_line(line)

            if parsed is None:  # Invalid line
                invalid_lines += 1
                continue

            # Normalize the level
            timestamp, level, service, message = parsed
            normalized_level = normalize_level(level)

            # Validate the level
            if normalized_level in ALLOWED_LEVELS:
                level_counts[normalized_level] += 1
            else:
                level_counts["INVALID_LEVEL"] += 1

    # TODO 7: Create the summary string
    summary = f"""
    Total lines: {total_lines}
    Invalid lines: {invalid_lines}
    INFO: {level_counts["INFO"]}
    WARN: {level_counts["WARN"]}
    ERROR: {level_counts["ERROR"]}
    INVALID_LEVEL: {level_counts["INVALID_LEVEL"]}
    """

    # TODO 8: Print the summary
    print(summary)

    # TODO 9: Save the summary into period1_report.txt
    with open(OUTPUT_REPORT, 'w') as output_file:
        output_file.write(summary)

if __name__ == "__main__":
    main()
