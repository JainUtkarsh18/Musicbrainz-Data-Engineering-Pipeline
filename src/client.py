class MusicBrainzClient:
    """
    MusicBrainz API client with:
    - valid User-Agent
    - rate limiting
    - retry handling
    - cached responses
    """ 

    def __init__(self) -> None:
        self.session = requests_cache.CachedSession(
            cache_name=str(OUTPUT_DIR / "musicbrainz_cache"),
            backend="sqlite",
            expire_after=60 * 60 * 24 * 7,
        )

        self.session.headers.update({"User-Agent": USER_AGENT})

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a GET request to the MusicBrainz API.
        """
        url = f"{BASE_URL}/{endpoint}"

        for attempt in range(MAX_RETRIES):
            try:
                time.sleep(REQUEST_DELAY_SECONDS)

                response = self.session.get(
                    url,
                    params=params,
                    timeout=REQUEST_TIMEOUT,
                )

                if response.status_code == 200:
                    return response.json()

                if response.status_code in (429, 502, 503, 504):
                    wait_time = min(30, 2 ** attempt)
                    logger.warning(
                        "HTTP %s. Retrying in %s seconds.",
                        response.status_code,
                        wait_time,
                    )
                    time.sleep(wait_time)
                    continue

                raise RuntimeError(
                    f"MusicBrainz error {response.status_code}: {response.text[:300]}"
                )

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError,
            ) as error:
                wait_time = min(30, 2 ** attempt)
                logger.warning(
                    "Network error: %s. Retrying in %s seconds.",
                    error,
                    wait_time,
                )
                time.sleep(wait_time)

        raise RuntimeError(f"Failed after {MAX_RETRIES} retries: {url}")
