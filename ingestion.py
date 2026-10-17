import json
from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path(
    "/Users/destinybrewington/PycharmProjects/Met_Female_Modern_Art"
)
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = DATA_DIR / "met_modern_art.csv"

# GitHub Media endpoint for the official Met Open Access dataset
GITHUB_LFS_URL = (
    "https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv"
)

use_cols = [
    "Object ID",
    "Title",
    "Artist Display Name",
    "Artist Gender",
    "Department",
    "Classification",
    "Medium",
    "Gallery Number",
    "Object Begin Date",
    "Object End Date",
    "Tags",
]

matched_chunks = []
chunk_size = 2500

print("Streaming MetObjects.csv for 20th & 21st Century artworks on view...")

for chunk in pd.read_csv(
    GITHUB_LFS_URL,
    usecols=use_cols,
    chunksize=chunk_size,
    low_memory=False,
    storage_options={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    },
):
    # 1. On Display Check
    gallery_str = (
        chunk["Gallery Number"].fillna("").astype(str).str.strip().str.lower()
    )
    is_on_display = (gallery_str != "") & (gallery_str != "nan")
    on_display = chunk[is_on_display].copy()

    if on_display.empty:
        continue

    # 2. Date Filtering: 20th and 21st Century (1900 to Present)
    # Coerce to numeric to prevent ValueError on string lifespans or empty values
    end_dates = pd.to_numeric(on_display["Object End Date"], errors="coerce")
    begin_dates = pd.to_numeric(on_display["Object Begin Date"], errors="coerce")

    # Match works created or finished in 1900 or later
    is_modern_era = (end_dates >= 1900) | (begin_dates >= 1900)
    era_works = on_display[is_modern_era].copy()

    if era_works.empty:
        continue

    # 3. Classify Artist Gender (Affirmative schema)
    raw_gender = (
        era_works["Artist Gender"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )
    artist_name = (
        era_works["Artist Display Name"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    is_female = raw_gender.str.contains("female", na=False)
    is_unattributed = (
        (artist_name == "")
        | (artist_name.str.lower() == "nan")
        | artist_name.str.lower().str.contains(
            "unknown|anonymous|unidentified|workshop|school of", na=False
        )
    )

    era_works["Gender Category"] = np.select(
        [is_female, is_unattributed],
        ["Female", "Unknown / Unattributed"],
        default="Male",
    )

    # 4. Subject Tags Parsing: Distinct Regex with Word Boundaries (\b)
    tags_str = era_works["Tags"].fillna("").astype(str).str.lower()
    era_works["Is_Female_Nude"] = tags_str.str.contains(
        r"\bfemale nudes?\b", regex=True, na=False
    )
    era_works["Is_Male_Nude"] = tags_str.str.contains(
        r"\bmale nudes?\b", regex=True, na=False
    )
    era_works["Is_Nude"] = (
        tags_str.str.contains(r"\bnudes?\b", regex=True, na=False)
        | era_works["Is_Female_Nude"]
        | era_works["Is_Male_Nude"]
    )

    matched_chunks.append(era_works)

# Combine chunks
audit_df = pd.concat(matched_chunks, ignore_index=True)
audit_df.to_csv(OUTPUT_PATH, index=False)

print("\n" + "=" * 55)
print("GUERRILLA GIRLS AUDIT: 20TH & 21ST CENTURY ARTWORKS ON VIEW")
print("=" * 55)
print(f"Total 20th/21st Century Artworks On View: {len(audit_df)}")

# Cohort of works by attributed artists
named_works = audit_df[audit_df["Gender Category"].isin(["Female", "Male"])].copy()

if not named_works.empty:
    # -------------------------------------------------------------
    # METRIC 1: Artwork-level Representation (% of works on view)
    # -------------------------------------------------------------
    total_named_works = len(named_works)
    female_works_count = len(
        named_works[named_works["Gender Category"] == "Female"]
    )
    pct_female_works = (female_works_count / total_named_works) * 100

    print("\n--- 1. ARTWORK LEVEL (Objects on Display) ---")
    print(
        f"Works by Female Artists: {pct_female_works:.2f}% ({female_works_count} of {total_named_works})"
    )

    # -------------------------------------------------------------
    # METRIC 2: Artist-level Representation (% of unique artists)
    # -------------------------------------------------------------
    unique_artists = named_works.drop_duplicates(
        subset=["Artist Display Name"]
    ).copy()
    total_unique_artists = len(unique_artists)
    female_unique_count = len(
        unique_artists[unique_artists["Gender Category"] == "Female"]
    )
    pct_female_artists = (female_unique_count / total_unique_artists) * 100

    print("\n--- 2. ARTIST LEVEL (Unique Individuals on Display) ---")
    print(
        f"Unique Female Artists:   {pct_female_artists:.2f}% ({female_unique_count} of {total_unique_artists})"
    )

    # Average Works per Artist
    male_unique_count = total_unique_artists - female_unique_count
    male_works_count = total_named_works - female_works_count
    works_per_female = (
        female_works_count / female_unique_count if female_unique_count else 0
    )
    works_per_male = (
        male_works_count / male_unique_count if male_unique_count else 0
    )

    print(
        f"Avg Works Per Creator:   Female: {works_per_female:.2f} | Male: {works_per_male:.2f}"
    )

# -----------------------------------------------------------------
# METRIC 3: Subject Nude Breakdown
# -----------------------------------------------------------------
nudes_cohort = audit_df[audit_df["Is_Nude"]]
if not nudes_cohort.empty:
    total_nudes = len(nudes_cohort)
    female_nudes_count = nudes_cohort["Is_Female_Nude"].sum()
    male_nudes_count = nudes_cohort["Is_Male_Nude"].sum()
    pct_female_nudes = (female_nudes_count / total_nudes) * 100
    pct_male_nudes = (male_nudes_count / total_nudes) * 100

    print("\n--- 3. SUBJECT LEVEL (Nudes on Display) ---")
    print(f"Total Nudes Identified:      {total_nudes}")
    print(f"Female Nude Subjects:        {pct_female_nudes:.2f}% ({female_nudes_count} of {total_nudes})")
    print(f"Male Nude Subjects:          {pct_male_nudes:.2f}% ({male_nudes_count} of {total_nudes})")
else:
    print("\nNo works with explicit nude tags detected.")

# Department Breakdown
print("\nTop Departments Housing 20th/21st Century Works by Female Artists:")
female_dept = audit_df[audit_df["Gender Category"] == "Female"]["Department"].value_counts()
print(female_dept.head(6))

print(audit_df[audit_df["Is_Nude"]==True])