print("Starting MusicBrainz ISRC data collection")
print("Labels:", LABELS)
print("Date range:", START_DATE, "to", END_DATE)

df = collect_musicbrainz_dataset()

if df.empty:
    print("No records were collected.")
    print("Try increasing the date range or changing the labels.")

else:
    print("\nData collection completed successfully.")

    # Save main Kaggle dataset files
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    df.to_parquet(OUTPUT_PARQUET, index=False)

    print("\nMain files saved:")
    print("CSV:", OUTPUT_CSV)
    print("Parquet:", OUTPUT_PARQUET)

    # EDA
    eda_tables = create_eda_tables(df)

    # Display dataset preview
    print("\n========== DATASET PREVIEW ==========")
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    display(df)

    print("\n========== DATASET SHAPE ==========")
    print(df.shape)

    print("\n========== TRACKS BY LABEL ==========")
    display(eda_tables["tracks_by_label"])

    print("\n========== TRACKS BY MONTH ==========")
    display(eda_tables["tracks_by_month"])

    print("\n========== ISRC COVERAGE BY LABEL ==========")
    display(eda_tables["isrc_coverage_by_label"])

    print("\n========== TOP ARTISTS ==========")
    display(eda_tables["top_artists"])

    print("\n========== SELECTED DATASET COLUMNS ==========")
    useful_columns = [
        "label",
        "release_date",
        "release_title",
        "track_number",
        "track_title",
        "artist",
        "isrc",
        "musicbrainz_release_url",
    ]

    display(df[useful_columns].head(30))

    # Visualizations
    print("\n========== VISUALIZATIONS ==========")
    save_and_show_plots(df, eda_tables)

    # Summary report
    report_text = create_summary_report(df, eda_tables)

    print("\n========== SUMMARY REPORT ==========")
    display(Markdown(report_text))

    print("\n========== FINAL KAGGLE OUTPUT FILES ==========")
    output_files = [
        OUTPUT_CSV,
        OUTPUT_PARQUET,
        SUMMARY_REPORT,
        TRACKS_BY_LABEL_PLOT,
        TRACKS_BY_MONTH_PLOT,
        ISRC_COVERAGE_PLOT,
        TOP_ARTISTS_PLOT,
        RELEASE_SIZE_PLOT,
    ]

    for file in output_files:
        print(file)
