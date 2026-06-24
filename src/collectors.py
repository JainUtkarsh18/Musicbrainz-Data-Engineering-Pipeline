def find_label_id(client: MusicBrainzClient, label_name: str) -> Tuple[str, str]:
    """
    Resolve a label name to a MusicBrainz label ID and official display name.
    """
    candidates = [label_name]
    candidates.extend(LABEL_ALIASES.get(label_name, []))

    for candidate in candidates:
        exact_data = client.get(
            "label",
            params={
                "query": f'label:"{candidate}"',
                "fmt": "json",
                "limit": 5,
            },
        )

        exact_labels = exact_data.get("labels", [])
        if exact_labels:
            best = exact_labels[0]
            return best["id"], best.get("name", candidate)

        loose_data = client.get(
            "label",
            params={
                "query": candidate,
                "fmt": "json",
                "limit": 5,
            },
        )

        loose_labels = loose_data.get("labels", [])
        if loose_labels:
            best = loose_labels[0]
            return best["id"], best.get("name", candidate)

    raise ValueError(f"No MusicBrainz label found for: {label_name}")


def search_releases_for_label(
    client: MusicBrainzClient,
    label_display_name: str,
    start_date: str,
    end_date: str,
) -> List[Dict[str, Any]]:
    """
    Search MusicBrainz releases for a selected label and date range.
    """
    all_releases = []
    limit = 100
    offset = 0

    query = f'label:"{label_display_name}" AND date:[{start_date} TO {end_date}]'

    while True:
        data = client.get(
            "release",
            params={
                "query": query,
                "fmt": "json",
                "limit": limit,
                "offset": offset,
            },
        )

        releases = data.get("releases", [])
        total_count = data.get("release-count", 0)

        all_releases.extend(releases)

        logger.info(
            "Fetched %s/%s releases for %s",
            len(all_releases),
            total_count,
            label_display_name,
        )

        offset += limit

        if len(all_releases) >= total_count or not releases:
            break

    return all_releases


def fetch_tracks_with_isrc(
    client: MusicBrainzClient,
    release_id: str,
) -> List[Dict[str, Any]]:
    """
    Fetch track-level metadata and ISRCs for a MusicBrainz release.
    """
    data = client.get(
        f"release/{release_id}",
        params={
            "fmt": "json",
            "inc": "recordings+isrcs+artist-credits",
        },
    )

    release_title = data.get("title", "")
    release_date = data.get("date", "")
    release_status = data.get("status", "")
    release_country = data.get("country", "")
    release_barcode = data.get("barcode", "")
    release_id = data.get("id", "")

    rows = []

    for media in data.get("media", []) or []:
        medium_format = media.get("format", "")
        medium_position = media.get("position", "")

        for track in media.get("tracks", []) or []:
            track_number = track.get("position")
            track_title = track.get("title", "")
            track_length_ms = track.get("length")

            recording = track.get("recording", {}) or {}
            recording_id = recording.get("id", "")

            isrcs = recording.get("isrcs", []) or []
            isrc_string = "; ".join(isrcs) if isrcs else ""

            artist = extract_artist_credit(recording, track)

            rows.append(
                {
                    "release_date": release_date,
                    "release_title": release_title,
                    "release_status": release_status,
                    "release_country": release_country,
                    "release_barcode": release_barcode,
                    "medium_format": medium_format,
                    "medium_position": medium_position,
                    "track_number": track_number,
                    "track_title": track_title,
                    "artist": artist,
                    "track_length_ms": track_length_ms,
                    "isrc": isrc_string,
                    "has_isrc": bool(isrcs),
                    "release_id": release_id,
                    "recording_id": recording_id,
                    "musicbrainz_release_url": f"https://musicbrainz.org/release/{release_id}",
                    "musicbrainz_recording_url": (
                        f"https://musicbrainz.org/recording/{recording_id}"
                        if recording_id
                        else ""
                    ),
                }
            )

    return rows


def collect_musicbrainz_dataset() -> pd.DataFrame:
    """
    Collect track-level MusicBrainz ISRC data for selected labels.
    """
    client = MusicBrainzClient()

    all_rows = []
    seen = set()

    for label in tqdm(LABELS, desc="Processing labels"):
        logger.info("Processing label: %s", label)

        try:
            label_id, label_display_name = find_label_id(client, label)
            logger.info("Resolved label: %s | ID: %s", label_display_name, label_id)

        except Exception as error:
            logger.exception("Label search failed for %s: %s", label, error)
            continue

        try:
            releases = search_releases_for_label(
                client=client,
                label_display_name=label_display_name,
                start_date=START_DATE,
                end_date=END_DATE,
            )

        except Exception as error:
            logger.exception("Release search failed for %s: %s", label, error)
            continue

        if MAX_RELEASES_PER_LABEL is not None:
            releases = releases[:MAX_RELEASES_PER_LABEL]

        logger.info(
            "Using %s releases for label %s",
            len(releases),
            label_display_name,
        )

        for release in tqdm(
            releases,
            desc=f"Fetching tracks: {label_display_name}",
            leave=False,
        ):
            release_id = release.get("id")

            if not release_id:
                continue

            try:
                track_rows = fetch_tracks_with_isrc(client, release_id)

            except Exception as error:
                logger.warning("Failed release %s: %s", release_id, error)
                continue

            for row in track_rows:
                dedupe_key = (
                    row.get("isrc") or row.get("recording_id"),
                    row.get("track_title"),
                    row.get("artist"),
                )

                if dedupe_key in seen:
                    continue

                seen.add(dedupe_key)

                row["label"] = label_display_name
                row["label_query"] = label
                row["label_id"] = label_id

                all_rows.append(row)

    df = pd.DataFrame(all_rows)

    if not df.empty:
        df["release_date_parsed"] = df["release_date"].apply(parse_date)

        df["release_year"] = pd.to_datetime(
            df["release_date_parsed"],
            errors="coerce",
        ).dt.year

        df["release_month"] = pd.to_datetime(
            df["release_date_parsed"],
            errors="coerce",
        ).dt.to_period("M").astype(str)

        df = df.sort_values(
            by=[
                "label",
                "release_date_parsed",
                "release_title",
                "track_number",
            ],
            na_position="last",
        )

    return df
