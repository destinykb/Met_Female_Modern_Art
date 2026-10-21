import html
from pathlib import Path
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# style
st.set_page_config(
    page_title="Do Women Still Have To Be Naked?",
    page_icon="🦍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        /* Base page background: Yellow */
        .stApp {
            background-color: #FFE800 !important;
            color: #000000 !important;
            font-family: 'Helvetica Neue', 'Arial Black', sans-serif;
        }

        /* Header typography */
        .poster-title {
            font-size: 3.1rem !important;
            font-weight: 900 !important;
            line-height: 1.0 !important;
            letter-spacing: -1.5px;
            color: #000000;
            margin-bottom: 0.2rem;
            text-transform: lowercase;
        }
        .poster-title span.italic-sub {
            font-style: italic;
            text-decoration: underline;
            text-underline-offset: 5px;
        }
        .poster-subtitle {
            font-size: 1.25rem !important;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #000000;
            border-bottom: 4px solid #000000;
            padding-bottom: 6px;
            margin-bottom: 1.2rem;
        }

        /* Shift the top-right image column up to align with header top */
        div[data-testid="column"]:nth-of-type(2) {
            margin-top: -6px;
        }

        /* Red Callout Metrics matching original poster colorway */
        .stat-card {
            background-color: #FFE800;
            border: 4px solid #000000;
            padding: 14px;
            box-shadow: 5px 5px 0px #000000;
            height: 100%;
        }
        .stat-number-red {
            font-size: 3.2rem;
            font-weight: 900;
            line-height: 0.95;
            color: #E00000 !important;
            letter-spacing: -1px;
        }
        .stat-label {
            font-size: 0.95rem;
            font-weight: 900;
            line-height: 1.2;
            margin-top: 8px;
            color: #000000;
            text-transform: uppercase;
        }
        .stat-subtext {
            font-size: 0.8rem;
            font-weight: 700;
            margin-top: 6px;
            color: #111111;
        }

        /* Section Dividers */
        .section-header {
            font-size: 1.7rem;
            font-weight: 900;
            text-transform: uppercase;
            border-bottom: 4px solid #000000;
            padding-bottom: 4px;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            color: #000000;
        }

        /* Gallery Grid & Hover Tooltip Styling */
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 18px;
            margin-top: 15px;
        }
        .artwork-container {
            position: relative;
            background-color: #000000;
            border: 3px solid #000000;
            box-shadow: 4px 4px 0px #000000;
            overflow: visible;
        }
        .artwork-container img {
            width: 100%;
            height: 270px;
            object-fit: cover;
            display: block;
            transition: transform 0.2s ease-in-out, opacity 0.2s;
        }
        .artwork-container:hover img {
            opacity: 0.85;
            transform: scale(1.02);
        }

        /* Enlarged Text-Only Black Card for works without photography */
        .no-photo-card {
            width: 100%;
            height: 270px;
            background: #000000;
            color: #FFE800;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: flex-start;
            text-align: left;
            padding: 16px;
            box-sizing: border-box;
            border: 1px solid #222222;
            overflow: hidden;
        }
        .no-photo-title {
            font-size: 0.95rem;
            font-weight: 900;
            color: #FFFFFF;
            line-height: 1.2;
            margin-top: 8px;
            margin-bottom: 6px;
        }
        .no-photo-body {
            font-size: 0.82rem;
            line-height: 1.4;
            color: #FFE800;
        }
        .no-photo-badge {
            font-size: 0.7rem;
            font-weight: 900;
            background: #222222;
            color: #FFE800;
            padding: 3px 8px;
            border-radius: 2px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        /* CSS Tooltip on Hover */
        .artwork-tooltip {
            visibility: hidden;
            opacity: 0;
            position: absolute;
            bottom: 105%;
            left: 50%;
            transform: translateX(-50%);
            width: 250px;
            background-color: #000000;
            color: #FFE800;
            border: 2px solid #FFE800;
            padding: 10px;
            border-radius: 2px;
            font-size: 0.8rem;
            font-weight: 600;
            line-height: 1.3;
            z-index: 1000;
            box-shadow: 4px 4px 0px rgba(0,0,0,0.6);
            transition: opacity 0.2s, visibility 0.2s;
            pointer-events: none;
        }
        .artwork-tooltip::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -6px;
            border-width: 6px;
            border-style: solid;
            border-color: #000000 transparent transparent transparent;
        }
        .artwork-container:hover .artwork-tooltip {
            visibility: visible;
            opacity: 1;
        }
        .badge-female {
            color: #FFE800;
            font-weight: 900;
        }
        .badge-subject-fem {
            color: #FF5555;
            font-weight: 900;
        }
        .poster-footer {
            margin-top: 40px;
            margin-bottom: 25px;
            padding: 14px 18px;
            border-top: 3.5px solid #000000;
            border-bottom: 3.5px solid #000000;
            background-color: #FFE800;
            color: #000000;
            font-size: 0.82rem;
            font-weight: 700;
            line-height: 1.5;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }

        .poster-footer a {
            color: #000000 !important;
            font-weight: 900;
            text-decoration: underline;
            text-underline-offset: 3px;
            transition: color 0.15s ease-in-out;
        }

        .poster-footer a:hover {
            color: #E00000 !important; /* Highlights in red on hover */
        }

        .poster-footer .footer-tagline {
            font-weight: 900;
            letter-spacing: 0.5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# load data

BASE_DIR = Path(__file__).resolve().parent

AUDIT_CSV = (
    BASE_DIR / "met_modern_art.csv"
    if (BASE_DIR / "met_modern_art.csv").exists()
    else BASE_DIR / "data" / "met_modern_art.csv"
)

NUDES_CSV = (
    BASE_DIR / "art_images.csv"
    if (BASE_DIR / "art_images.csv").exists()
    else BASE_DIR / "data" / "art_images.csv"
)


@st.cache_data
def load_data():
  if not AUDIT_CSV.exists():
    st.error(
        f"Data file not found at: {AUDIT_CSV}. Ensure it is committed to GitHub."
    )
    st.stop()

  df_audit = pd.read_csv(AUDIT_CSV, low_memory=False)
  for col in ["Is_Female_Nude", "Is_Male_Nude", "Is_Nude"]:
    df_audit[col] = df_audit[col].fillna(False).astype(bool)

  if NUDES_CSV.exists():
    df_nudes = pd.read_csv(NUDES_CSV, low_memory=False)
    for col in ["Is_Female_Nude", "Is_Male_Nude", "Is_Nude"]:
      df_nudes[col] = df_nudes[col].fillna(False).astype(bool)
    df_nudes["primaryImageSmall"] = (
        df_nudes["primaryImageSmall"].fillna("").astype(str)
    )
  else:
    df_nudes = df_audit[df_audit["Is_Nude"]].copy()
    df_nudes["primaryImageSmall"] = ""

  return df_audit, df_nudes


df_audit, df_nudes = load_data()

# primary dash
col_header_left, col_header_right = st.columns([2.3, 1.2])

with col_header_left:
    st.markdown(
        '<div class="poster-title">Do women <span class="italic-sub">still</span> have to be naked to get into the Met. Museum?</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="poster-subtitle"> Gender Disparities in the 20th & 21st Century Art of the Met Collection</div>',
        unsafe_allow_html=True,
    )

    # key metrics
    named_works = df_audit[
        df_audit["Gender Category"].isin(["Female", "Male"])
    ].copy()
    total_named = len(named_works)
    fem_works = len(named_works[named_works["Gender Category"] == "Female"])
    pct_fem_works = (fem_works / total_named) * 100 if total_named else 0.0

    unique_artists = named_works.drop_duplicates(
        subset=["Artist Display Name"]
    ).copy()
    total_artists = len(unique_artists)
    fem_artists = len(
        unique_artists[unique_artists["Gender Category"] == "Female"]
    )
    pct_fem_artists = (
        (fem_artists / total_artists) * 100 if total_artists else 0.0
    )

    nudes_all = df_audit[df_audit["Is_Nude"]]
    total_nudes = len(nudes_all)
    fem_nudes = nudes_all["Is_Female_Nude"].sum()
    pct_fem_nudes = (fem_nudes / total_nudes) * 100 if total_nudes else 0.0

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number-red">{pct_fem_works:.1f}%</div>
                <div class="stat-label">of artworks on display are by women</div>
                <div class="stat-subtext">({fem_works} of {total_named} works)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m_col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number-red">{pct_fem_artists:.1f}%</div>
                <div class="stat-label">of unique artists on display are women</div>
                <div class="stat-subtext">({fem_artists} of {total_artists} individuals)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m_col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number-red">{pct_fem_nudes:.1f}%</div>
                <div class="stat-label">of nude artworks contain female subjects</div>
                <div class="stat-subtext">({fem_nudes} female vs {nudes_all['Is_Male_Nude'].sum()} male)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # place on left

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-header" style="margin-top:0;">Female Artists vs. Female Nudes by Department</div>',
        unsafe_allow_html=True,
    )

    top_depts = df_audit["Department"].value_counts().head(6).index.tolist()
    dept_rows = []

    for dept in top_depts:
        sub = df_audit[df_audit["Department"] == dept]
        sub_named = sub[sub["Gender Category"].isin(["Female", "Male"])]
        sub_nudes = sub[sub["Is_Nude"]]

        pct_f_artists = (
            (sub_named["Gender Category"] == "Female").mean() * 100
            if not sub_named.empty
            else 0.0
        )
        pct_f_nudes = (
            (sub_nudes["Is_Female_Nude"].sum() / len(sub_nudes)) * 100
            if not sub_nudes.empty
            else 0.0
        )

        dept_rows.append({
            "Department": dept,
            "Metric": "% of Female Artists on View",
            "Percentage": round(pct_f_artists, 1),
        })
        dept_rows.append({
            "Department": dept,
            "Metric": "% of Female Nudes On View",
            "Percentage": round(pct_f_nudes, 1),
        })

    chart_df = pd.DataFrame(dept_rows)

    chart = (
        alt.Chart(chart_df)
        .mark_bar(stroke="#000000", strokeWidth=1.5)
        .encode(
            x=alt.X(
                "Percentage:Q",
                title="Percentage (%)",
                scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(
                    tickColor="#000",
                    labelColor="#000",
                    titleColor="#000",
                    titleFontWeight="bold",
                    grid=True,
                    gridColor="#d4c000",
                ),
            ),
            y=alt.Y(
                "Department:N",
                title=None,
                sort="-x",
                axis=alt.Axis(
                    labelColor="#000",
                    labelFontSize=12,
                    labelFontWeight="bold",
                    labelLimit=320,
                    tickColor="#000",
                ),
            ),
            yOffset="Metric:N",
            color=alt.Color(
                "Metric:N",
                scale=alt.Scale(
                    domain=[
                        "% of Female Artists on View",
                        "% of Female Nudes On View",
                    ],
                    range=["#000000", "#E00000"],
                ),
                legend=alt.Legend(
                    title=None,
                    orient="bottom",
                    direction="horizontal",
                    labelColor="#000000",
                    labelFontSize=12,
                    labelFontWeight="bold",
                    offset=-6,
                ),
            ),
            tooltip=[
                alt.Tooltip("Department:N", title="Department"),
                alt.Tooltip("Metric:N", title="Category"),
                alt.Tooltip("Percentage:Q", format=".1f", title="% Share"),
            ],
        )
        .properties(height=340, background="#FFE800")
        .configure_view(strokeOpacity=0)
    )

    st.altair_chart(chart, use_container_width=True)

with col_header_right:
  local_img_candidates = [
      BASE_DIR / "figure_sketch2.PNG",
      BASE_DIR / "figure_sketch2.png",
      BASE_DIR / "assets" / "figure_sketch2.PNG",
      BASE_DIR / "assets" / "figure_sketch2.png",
  ]
  found_img = next((p for p in local_img_candidates if p.exists()), None)

  if found_img:
    st.image(str(found_img), use_container_width=True)
  else:
    st.markdown(
        """
            <div style="border: 4px solid #000; padding: 30px; background: #000; color: #FFE800; text-align: center; box-shadow: 6px 6px 0px #000;">
                <h1 style="font-size: 3.5rem; margin: 0;">🦍</h1>
                <p style="font-weight: 900; margin: 5px 0 0 0; text-transform: uppercase;">
                    Place figure_sketch.PNG in your root project folder to render here
                </p>
            </div>
            """,
        unsafe_allow_html=True,
    )

# gallery

st.markdown(
    '<div class="section-header">On-View Nude Artworks</div>',
    unsafe_allow_html=True,
)

col_filt1, col_filt2 = st.columns([1, 2])
with col_filt1:
    subject_filter = st.radio(
        "Filter Gallery by Subject:",
        ["All Nudes", "Female Nude Subjects", "Male Nude Subjects"],
        horizontal=True,
    )

gallery_items = df_nudes.copy()
if subject_filter == "Female Nudes Only":
    gallery_items = gallery_items[gallery_items["Is_Female_Nude"] == True]
elif subject_filter == "Male Nudes Only":
    gallery_items = gallery_items[gallery_items["Is_Male_Nude"] == True]

gallery_items["has_photo"] = gallery_items["primaryImageSmall"].fillna("").astype(str).str.startswith("http")
gallery_items = gallery_items.sort_values(by="has_photo", ascending=False).reset_index(drop=True)

with col_filt2:
    with_img_count = int(gallery_items["has_photo"].sum())
    st.markdown(
        f"<div style='font-weight: 800; padding-top: 10px; color: #000;'>"
        f"Displaying {len(gallery_items)} works ({with_img_count} with photography up top, "
        f"{len(gallery_items) - with_img_count} text cards below).</div>",
        unsafe_allow_html=True,
    )

# cards
cards_html = ['<div class="gallery-grid">']

for _, item in gallery_items.iterrows():
    title_raw = str(item.get("Title", "Untitled"))
    title_esc = html.escape(title_raw)
    artist_esc = html.escape(str(item.get("Artist Display Name", "Unknown")))
    dept_esc = html.escape(str(item.get("Department", "Unknown")))
    gallery_esc = html.escape(str(item.get("Gallery Number", "On View")))
    gender_esc = html.escape(str(item.get("Gender Category", "Male")))
    img_url = str(item.get("primaryImageSmall", ""))
    has_photo = item.get("has_photo", False)

    # Date extraction
    begin_d = item.get("Object Begin Date", "")
    end_d = item.get("Object End Date", "")
    try:
        b_val = int(float(begin_d)) if pd.notna(begin_d) and str(begin_d).strip() != "" else None
        e_val = int(float(end_d)) if pd.notna(end_d) and str(end_d).strip() != "" else None
        if b_val and e_val:
            date_str = f"{b_val}" if b_val == e_val else f"{b_val}–{e_val}"
        elif e_val:
            date_str = f"{e_val}"
        elif b_val:
            date_str = f"{b_val}"
        else:
            date_str = "Date n/a"
    except (ValueError, TypeError):
        date_str = "Date n/a"

    subject_class = (
        "Female Nude"
        if item["Is_Female_Nude"]
        else ("Male Nude" if item["Is_Male_Nude"] else "Unspecified Nude")
    )
    subject_badge = (
        f'<span class="badge-subject-fem">{subject_class}</span>'
        if item["Is_Female_Nude"]
        else f"<span>{subject_class}</span>"
    )

    if has_photo:
        media_block = f'<img src="{img_url}" loading="lazy" alt="{title_esc}" />'
    else:
        media_block = f"""
        <div class="no-photo-card">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="no-photo-badge">Rights Restricted</div>
                    <span style="font-size: 0.75rem; font-weight: 800; color: #FFE800;">{date_str}</span>
                </div>
                <div class="no-photo-title">{title_esc[:55]}{'...' if len(title_raw) > 55 else ''}</div>
            </div>
            <div class="no-photo-body">
                <div><strong>By:</strong> {artist_esc} ({gender_esc})</div>
                <div><strong>Subject:</strong> {subject_badge}</div>
            </div>
        </div>
        """

    cards_html.append(f"""
        <div class="artwork-container">
            {media_block}
            <div class="artwork-tooltip">
                <div style="font-size: 0.9rem; font-weight: 900; margin-bottom: 4px; color: #FFF;">{title_esc}</div>
                <div><strong>Date:</strong> {date_str}</div>
                <div><strong>Artist:</strong> {artist_esc} (<span class="badge-female">{gender_esc}</span>)</div>
                <div><strong>Subject:</strong> {subject_badge}</div>
                <div><strong>Department:</strong> {dept_esc}</div>
            </div>
        </div>
    """)

cards_html.append("</div>")

st.html("".join(cards_html))

st.markdown(
    """
    <div class="poster-footer">
        <div>
            <strong>DATA SOURCE:</strong> <a href="https://github.com/metmuseum/openaccess" target="_blank">The Metropolitan Museum of Art Open Access CSV</a> & <a href="https://metmuseum.github.io/" target="_blank">REST Collection API</a>
            &nbsp;|&nbsp;
            <strong>ILLUSTRATION:</strong> Destiny Brewington (<a href="https://github.com/destinykb" target="_blank">GitHub</a>)
            &nbsp;|&nbsp;
            <strong>AESTHETIC INSPIRATION:</strong> Guerrilla Girls, <em>Do women have to be naked to get into the Met. Museum?</em> (1989)
        </div>
        <div class="footer-tagline">
            Destiny Brewington, October 2026
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)