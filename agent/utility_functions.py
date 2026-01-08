def timestamp_to_seconds(timestamp: str) -> int:
    """
    Converts 'HH:MM:SS', 'MM:SS', or 'S' formats to total seconds.
    Use this to generate the '?t=seconds' parameter for YouTube URLs.

    Examples:
    '01:02:03' -> 3723
    '05:10'    -> 310

    'https://youtu.be/abc (at 01:02:03)' -> https://youtu.be/abc?t=3723
    'https://youtu.be/abc (at 05:10)'    -> https://youtu.be/abc?t=310
    'https://youtu.be/abc (at 00:45)'    -> https://youtu.be/abc?t=45
    """
    parts = timestamp.split(":")
    # Multipliers for seconds, minutes, hours (reversed to match split order)
    multipliers = [1, 60, 3600]

    # Reverse the parts so seconds is always index 0
    parts = parts[::-1]

    total_seconds = sum(
        int(part) * multiplier for part, multiplier in zip(parts, multipliers)
    )
    return total_seconds


def fix_youtube_links(text: str) -> str:
    words = text.split()
    processed_words = []

    for word in words:
        # Check if the word is a YouTube link with the specific suffix
        if ("youtube.com" in word or "youtu.be" in word) and "?t=" in word:
            # 1. Split the URL into the base and the timestamp
            # Example: "https://youtu.be/abc?t=1:02" -> ["...abc", "1:02"]
            base_url, timestamp_raw = word.split("?t=", 1)

            # 2. Clean up any trailing punctuation (like a period or closing bracket)
            timestamp_clean = timestamp_raw.rstrip(".,)]")
            trailing_char = timestamp_raw[len(timestamp_clean) :]

            try:
                # 3. Convert and Reconstruct
                seconds = timestamp_to_seconds(timestamp_clean)

                # Use &t= for long URLs that already have ?v=, otherwise ?t=
                sep = "&t=" if "watch?v=" in base_url else "?t="
                new_word = f"{base_url}{sep}{seconds}{trailing_char}"
                processed_words.append(new_word)
            except (ValueError, IndexError):
                # If splitting fails or timestamp isn't valid, keep original
                processed_words.append(word)
        else:
            processed_words.append(word)

    return " ".join(processed_words)


if __name__ == "__main__":
    sample = "Check the answer at https://youtu.be/dQw4w9WgXcQ?t=1:02:03. Also see https://youtube.com/watch?v=H63RbTuHTy0?t=520"
    print(fix_youtube_links(sample))
