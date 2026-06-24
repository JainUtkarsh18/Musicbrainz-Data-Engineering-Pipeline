def parse_date(date_value: Optional[str]):
    """
    Parse a MusicBrainz date string.

    MusicBrainz dates may appear as:
    YYYY-MM-DD, YYYY-MM, or YYYY.
    """
    if not date_value:
        return None

    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(date_value, fmt).date()
        except ValueError:
            continue

    return None


def extract_artist_credit(recording: Dict[str, Any], track: Dict[str, Any]) -> str:
    """
    Extract artist names from MusicBrainz recording or track artist-credit field.
    """
    artist_credit = recording.get("artist-credit") or track.get("artist-credit") or []

    artists = []

    for item in artist_credit:
        if isinstance(item, dict) and "name" in item:
            artists.append(item["name"])

    return ", ".join(artists)
