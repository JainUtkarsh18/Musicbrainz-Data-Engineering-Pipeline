from src.config import *
# -----------------------------
# 3. Configuration
# -----------------------------

# Kaggle output directory
OUTPUT_DIR = Path("/kaggle/working")

# Use a project contact email.
# Do not publish your personal email if you do not want it public.
CONTACT = "contact@example.com"

BASE_URL = "https://musicbrainz.org/ws/2"
USER_AGENT = f"IndianMusicISRCFetcher/2.0 ({CONTACT})"

REQUEST_DELAY_SECONDS = 1.05
MAX_RETRIES = 7
REQUEST_TIMEOUT = 40

# Change labels and date range here
LABELS = [
    "Zee Music Company",
    "Sony Music India",
    "Saregama",
    "Tips Music",
    "Times Music",
    "Junglee Music",
    "YRF Music",
    "Ishtar Music",
    "Eros Now Music",
]

START_DATE = "2025-01-01"
END_DATE = "2026-01-31"

# Use None to collect all releases.
# Use a number like 10, 20, or 50 to reduce dataset size.
MAX_RELEASES_PER_LABEL = None

OUTPUT_BASENAME = f"musicbrainz_isrc_{START_DATE}_to_{END_DATE}"

OUTPUT_CSV = OUTPUT_DIR / f"{OUTPUT_BASENAME}.csv"
OUTPUT_PARQUET = OUTPUT_DIR / f"{OUTPUT_BASENAME}.parquet"
SUMMARY_REPORT = OUTPUT_DIR / f"{OUTPUT_BASENAME}_summary_report.md"

TRACKS_BY_LABEL_PLOT = OUTPUT_DIR / "tracks_by_label.png"
TRACKS_BY_MONTH_PLOT = OUTPUT_DIR / "tracks_by_month.png"
ISRC_COVERAGE_PLOT = OUTPUT_DIR / "isrc_coverage_by_label.png"
TOP_ARTISTS_PLOT = OUTPUT_DIR / "top_artists.png"
RELEASE_SIZE_PLOT = OUTPUT_DIR / "release_size_distribution.png"

LABEL_ALIASES = {
    "Sony Music India": [
        "Sony Music Entertainment India",
        "Sony Music Entertainment",
        "Sony Music",
    ],
    "Tips Music": [
        "Tips Industries",
        "Tips",
    ],
    "Zee Music Company": [
        "Zee Music",
        "Zee Music Co.",
    ],
    "YRF Music": [
        "Yash Raj Films",
        "Yash Raj Music",
    ],
    "Eros Now Music": [
        "Eros Music",
        "Eros International",
    ],
}