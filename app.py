from pathlib import Path
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS Injection (Guerrilla Girls Visual Aesthetic)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Do Women Still Have To Be Naked?",
    page_icon="🦍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling: Pure Guerrilla Girls Black-on-Yellow high-contrast theme
st.markdown(
    """
    <style>
        /* Base page theme */
        .stApp {
            background-color: #FFE800 !important;
            color: #000000 !important;
            font-family: 'Arial Black', 'Impact', sans-serif;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #F4DE00 !important;
            border-right: 4px solid #000000;
        }
        section[data-testid="stSidebar"] * {
            color: #000000 !important;
        }

        /* Main Headline Header */
        .poster-title {
            font-size: 3.4rem !important;
            font-weight: 900 !important;
            line-height: 1.05 !important;
            text-transform: lowercase;
            letter-spacing: -1.5px;
            color: #000000;
            margin-bottom: 0.2rem;
        }
        .poster-title span.italic-sub {
            font-style: italic;
            text-decoration: underline;
            text-underline-offset: 6px;
        }

        .poster-subtitle {
            font-size: 1.6rem !important;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 1.5rem;
            border-bottom: 5px solid #000000;
            padding-bottom: 8px;
        }

        /* Metric Hero Cards */
        .stat-card {
            background-color: #FFE800;
            border: 4px solid #000000;
            padding: 18px;
            margin-bottom: 15px;
            box-shadow: 6px 6px 0px #000000;
        }
        .stat-number {
            font-size: 3.8rem;
            font-weight: 900;
            line-height: 0.95;
            color: #000000;
        }
        .stat-label {
            font-size: 1.05rem;
            font-weight: 800;
            line-height: 1.25;
            margin-top: 10px;
            color: #000000;
        }
        .stat-subtext {
            font-size: 0.85rem;
            font-weight: 700;
            margin-top: 6px;
            color: #222222;
        }

        /* Department Table Styling */
        div[data-testid="stDataFrame"] {
            border: 3px solid #000000;
            box-shadow: 5px 5px 0px #000000;
        }

        /* Radio & Selectbox overrides */
        .stSelectbox label, .stSlider label {
            font-weight: 900 !important;
            text-transform: uppercase;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. Data Loading & Cached Pipeline
# -----------------------------------------------------------------------------
DATA_PATH = Path(
    "/Users/destinybrewington/PycharmProjects/Met_Female_Modern_Art/met_modern_art.csv"
)


@st.cache_data
def load_audit_data():
  if not DATA_PATH.exists():
    st.error(f"Data file not found at: {DATA_PATH}")
    st.stop()
  df = pd.read_csv(DATA_PATH, low_memory=False)

  # Coerce dates and types cleanly
  df["Object Begin Date"] = pd.to_numeric(
      df["Object Begin Date"], errors="coerce"
  )
  df["Object End Date"] = pd.to_numeric(df["Object End Date"], errors="coerce")
  df["Is_Female_Nude"] = df["Is_Female_Nude"].fillna(False).astype(bool)
  df["Is_Male_Nude"] = df["Is_Male_Nude"].fillna(False).astype(bool)
  df["Is_Nude"] = df["Is_Nude"].fillna(False).astype(bool)
  return df


df = load_audit_data()

# -----------------------------------------------------------------------------
# 3. Interactive Sidebar Controls
# -----------------------------------------------------------------------------
st.sidebar.markdown("## 🦍 AUDIT CONTROLS")
st.sidebar.markdown("---")

# Department Filter
departments = sorted([d for d in df["Department"].dropna().unique() if d != ""])
selected_depts = st.sidebar.multiselect(
    "Filter Curatorial Department:",
    options=departments,
    default=departments,  # Select all by default
)

# Classification / Medium Filter
top_classifications = df["Classification"].value_counts().head(12).index.tolist()
selected_classes = st.sidebar.multiselect(
    "Filter Classification / Medium:",
    options=top_classifications,
    default=top_classifications,
)

# Date Slider
min_date = int(
    df["Object Begin Date"].dropna().min()
    if not df["Object Begin Date"].dropna().empty
    else 1900
)
max_date = int(
    df["Object End Date"].dropna().max()
    if not df["Object End Date"].dropna().empty
    else 2026
)
selected_dates = st.sidebar.slider(
    "Creation Date Range:",
    min_value=max(1880, min_date),
    max_value=max_date,
    value=(1900, max_date),
)

# Apply Filters
filtered_df = df[
    (df["Department"].isin(selected_depts))
    & (df["Classification"].isin(selected_classes))
    & (
        (df["Object End Date"] >= selected_dates[0])
        | (df["Object Begin Date"] >= selected_dates[0])
    )
    & (df["Object Begin Date"] <= selected_dates[1])
].copy()

# -----------------------------------------------------------------------------
# 4. Poster Headline & Layout
# -----------------------------------------------------------------------------
st.markdown(
    '<div class="poster-title">do women <span class="italic-sub">still</span> have to be naked to get into the Met. Museum?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="poster-subtitle">20th & 21st CENTURY ART ON VIEW ({selected_dates[0]}–{selected_dates[1]})</div>',
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 5. Core Guerrilla Girls Metric Cards (The 3 Punchlines)
# -----------------------------------------------------------------------------
named_works = filtered_df[
    filtered_df["Gender Category"].isin(["Female", "Male"])
].copy()

total_named_works = len(named_works)
female_works_count = len(
    named_works[named_works["Gender Category"] == "Female"]
)
pct_female_works = (
    (female_works_count / total_named_works * 100)
    if total_named_works > 0
    else 0.0
)

# Unique Creator Representation
unique_artists = named_works.drop_duplicates(
    subset=["Artist Display Name"]
).copy()
total_unique_creators = len(unique_artists)
female_creators_count = len(
    unique_artists[unique_artists["Gender Category"] == "Female"]
)
pct_female_creators = (
    (female_creators_count / total_unique_creators * 100)
    if total_unique_creators > 0
    else 0.0
)

# Nudes Representation
nudes_cohort = filtered_df[filtered_df["Is_Nude"]].copy()
total_nudes = len(nudes_cohort)
female_nudes_count = nudes_cohort["Is_Female_Nude"].sum()
male_nudes_count = nudes_cohort["Is_Male_Nude"].sum()
pct_female_nudes = (
    (female_nudes_count / total_nudes * 100) if total_nudes > 0 else 0.0
)

col1, col2, col3 = st.columns(3)

with col1:
  st.markdown(
      f"""
        <div class="stat-card">
            <div class="stat-number">{pct_female_works:.1f}%</div>
            <div class="stat-label">OF ARTWORKS ON DISPLAY ARE BY WOMEN</div>
            <div class="stat-subtext">({female_works_count:,} of {total_named_works:,} attributed works on view)</div>
            <div class="stat-subtext"><em>1989 Poster Baseline: &lt; 5%</em></div>
        </div>
    """,
      unsafe_allow_html=True,
  )

with col2:
  st.markdown(
      f"""
        <div class="stat-card">
            <div class="stat-number">{pct_female_creators:.1f}%</div>
            <div class="stat-label">OF UNIQUE ARTISTS ON DISPLAY ARE WOMEN</div>
            <div class="stat-subtext">({female_creators_count:,} of {total_unique_creators:,} individuals)</div>
            <div class="stat-subtext">Avg works: <strong>{female_works_count / max(female_creators_count, 1):.2f}</strong> (F) vs <strong>{(total_named_works - female_works_count) / max(total_unique_creators - female_creators_count, 1):.2f}</strong> (M)</div>
        </div>
    """,
      unsafe_allow_html=True,
  )

with col3:
  st.markdown(
      f"""
        <div class="stat-card">
            <div class="stat-number">{pct_female_nudes:.1f}%</div>
            <div class="stat-label">OF THE NUDES ON VIEW ARE FEMALE</div>
            <div class="stat-subtext">({female_nudes_count} female nudes vs {male_nudes_count} male nudes)</div>
            <div class="stat-subtext"><em>1989 Poster Baseline: 85%</em></div>
        </div>
    """,
      unsafe_allow_html=True,
  )

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. Breakdown: Department Distribution & Displayed Artists
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Department Contingency",
    "👩‍🎨 Female Artists on Floor",
    "🔍 Subject Nudes Catalog",
])

with tab1:
  st.markdown("### Curatorial Department Breakdown")
  dept_crosstab = (
      pd.crosstab(
          filtered_df["Department"],
          filtered_df["Gender Category"],
          margins=True,
          margins_name="Total",
      )
      .reset_index()
  )

  if "Female" in dept_crosstab.columns and "Total" in dept_crosstab.columns:
    dept_crosstab["% Female Works"] = (
        dept_crosstab["Female"] / dept_crosstab["Total"] * 100
    ).round(2)
    dept_crosstab = dept_crosstab.sort_values(
        by="% Female Works", ascending=False
    )

  st.dataframe(dept_crosstab, use_container_width=True, hide_index=True)

with tab2:
  st.markdown("### Female Artists Currently Displayed in Selected Scope")
  fem_df = filtered_df[filtered_df["Gender Category"] == "Female"]
  if not fem_df.empty:
    artist_counts = (
        fem_df.groupby(["Artist Display Name", "Department"])
        .size()
        .reset_index(name="Works on View")
        .sort_values(by="Works on View", ascending=False)
    )
    st.dataframe(artist_counts, use_container_width=True, hide_index=True)
  else:
    st.write("No female artists match the selected filters.")

with tab3:
  st.markdown("### Works Featuring Nude Subjects on Display")
  if not nudes_cohort.empty:
    nudes_view = nudes_cohort[[
        "Object ID",
        "Title",
        "Artist Display Name",
        "Gender Category",
        "Is_Female_Nude",
        "Is_Male_Nude",
        "Department",
        "Gallery Number",
    ]].copy()
    nudes_view["Subject Gender"] = np.select(
        [
            nudes_view["Is_Female_Nude"] & nudes_view["Is_Male_Nude"],
            nudes_view["Is_Female_Nude"],
            nudes_view["Is_Male_Nude"],
        ],
        ["Both Male & Female", "Female Nude", "Male Nude"],
        default="Unspecified Nude",
    )
    st.dataframe(
        nudes_view.drop(columns=["Is_Female_Nude", "Is_Male_Nude"]),
        use_container_width=True,
        hide_index=True,
    )
  else:
    st.write("No nude works tagged in this current slice.")

st.markdown("---")
st.markdown(
    "<small>Data Source: The Metropolitan Museum of Art Open Access Collection Dataset. Audit methodology inspired by Guerrilla Girls (1989).</small>",
    unsafe_allow_html=True,
)