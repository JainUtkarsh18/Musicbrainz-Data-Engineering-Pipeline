def create_summary_report(
    df: pd.DataFrame,
    eda_tables: Dict[str, pd.DataFrame],
) -> str:
    """
    Create and save a Markdown summary report.
    """
    total_tracks = len(df)
    total_labels = df["label"].nunique()
    total_releases = df["release_id"].nunique()
    total_artists = df["artist"].nunique()
    isrc_coverage = df["has_isrc"].mean() * 100

    tracks_by_label = eda_tables["tracks_by_label"]
    isrc_by_label = eda_tables["isrc_coverage_by_label"]
    top_artists = eda_tables["top_artists"]

    report = f"""# MusicBrainz Indian Music Label ISRC Dataset

## Dataset Overview

This dataset contains track-level metadata and ISRC information collected from the MusicBrainz API.

**Collection period:** {START_DATE} to {END_DATE}

| Metric | Value |
|---|---:|
| Total tracks | {total_tracks} |
| Total labels | {total_labels} |
| Total releases | {total_releases} |
| Total artists | {total_artists} |
| Overall ISRC coverage | {isrc_coverage:.2f}% |

---

## Labels Included

{", ".join(LABELS)}

---

## Tracks by Label

{tracks_by_label.to_markdown(index=False)}

---

## ISRC Coverage by Label

{isrc_by_label.to_markdown(index=False)}

---

## Top Artists

{top_artists.to_markdown(index=False)}

---

## Dataset Files

The notebook creates the following Kaggle output files:

- `{OUTPUT_CSV.name}`
- `{OUTPUT_PARQUET.name}`
- `{SUMMARY_REPORT.name}`
- `{TRACKS_BY_LABEL_PLOT.name}`
- `{TRACKS_BY_MONTH_PLOT.name}`
- `{ISRC_COVERAGE_PLOT.name}`
- `{TOP_ARTISTS_PLOT.name}`
- `{RELEASE_SIZE_PLOT.name}`

---

## Notes and Limitations

- The dataset depends on the completeness of MusicBrainz metadata.
- Some labels may have fewer records because MusicBrainz may not contain all releases.
- Some releases may not include ISRCs.
- Label matching depends on MusicBrainz naming conventions.
- CSV is suitable for general reuse.
- Parquet is suitable for larger analytical workflows.

---

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    SUMMARY_REPORT.write_text(report, encoding="utf-8")

    return report
