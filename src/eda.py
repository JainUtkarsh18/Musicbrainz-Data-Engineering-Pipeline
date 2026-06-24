def create_eda_tables(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Create summary tables for Kaggle notebook display.
    """
    eda_tables = {}

    eda_tables["tracks_by_label"] = (
        df.groupby("label")
        .size()
        .reset_index(name="track_count")
        .sort_values("track_count", ascending=False)
    )

    eda_tables["tracks_by_month"] = (
        df.groupby("release_month")
        .size()
        .reset_index(name="track_count")
        .sort_values("release_month")
    )

    eda_tables["isrc_coverage_by_label"] = (
        df.groupby("label")["has_isrc"]
        .mean()
        .mul(100)
        .reset_index(name="isrc_coverage_percent")
        .sort_values("isrc_coverage_percent", ascending=False)
    )

    eda_tables["top_artists"] = (
        df[df["artist"].notna() & (df["artist"] != "")]
        .groupby("artist")
        .size()
        .reset_index(name="track_count")
        .sort_values("track_count", ascending=False)
        .head(20)
    )

    eda_tables["release_size_distribution"] = (
        df.groupby(["release_id", "release_title"])
        .size()
        .reset_index(name="tracks_per_release")
        .sort_values("tracks_per_release", ascending=False)
    )

    return eda_tables
