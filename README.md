# Do Women Still Have to Be Naked to Get Into the Met. Museum? 
Destiny Brewington

<img width="2626" height="1397" alt="image" src="https://github.com/user-attachments/assets/65a94d29-129b-442f-831b-a5b69ab9778d" />


An interactive Streamlit data audit examining gender representation and nude subject depiction across 20th and 21st-century modern artworks currently on view at The Metropolitan Museum of Art. 

This project revisits the findings of the Guerrilla Girls' historic 1989 poster, **Do women have to be naked to get into the Met. Museum?** https://www.metmuseum.org/art/collection/search/849438, replicating their public audit framework computationally using the Met’s Open Access collection data.

**Live Dashboard**: https://womenofthemet.streamlit.app
**Artwork**: Destiny Brewington

---

## Summary & Key Findings

Auditing **2,888 on-view artworks** created from 1900 to the present across all curatorial departments revealed persistent disparities between creators and subjects:

* **8.05%** of on-view artworks from the 20th and 21st centuries are by women (182 of 2,261 attributed works).
* **11.26%** of unique artists with works on display are women (128 of 1,137 individuals).
* **1.42 vs. 2.06:** Average works displayed per female artists vs. per male artist.
* **77.39%** of on-view nude artworks depict female subjects (89 of 115 total nude works), while only 25.22% depict male subjects.

---

## Data Pipeline

1. **Data Loading**
   * Streamed directly from the official **Metropolitan Museum of Art Open Access** Git LFS dataset (~300 MB) using chunked `pandas` batch streaming.
2. **Filtering**
   * **On-Display Verification:** Artworks isolated via active, non-null `Gallery Number` assignments.
   * **Era Boundary:** Filtered for modern and contemporary works where `Object Begin Date` or `Object End Date` $\ge 1900$.
3. **Gender Schema & Subject Classification:**
   * Standardized creator gender using an affirmative schema (`Female`, `Male`, `Unknown / Unattributed`).
   * Parsed multi-valued tag strings using regex word boundaries (`\bfemale nudes?\b` vs. `\bmale nudes?\b`) to resolve substring naming collisions and handle singular/plural variations.
4. **Images:**
   * Enriched the nude artworks cohort by querying the Met Collection REST API for public domain and Creative Commons thumbnail endpoints (`primaryImageSmall`), providing graceful fallback metadata cards for copyright-restricted works.

---

## Dashboard

* **High-Contrast Guerrilla Girls Aesthetic:** Styled with the signature `#FFE800` yellow backdrop, bold grotesk typography, and high-impact red statistical callouts.
* **Curatorial Disparity Visualizations:** Interactive grouped bar chart breaking down the ratio of female artists vs. female nude subjects across top curatorial departments.
* **Interactive Gallery:** Responsive thumbnail grid featuring hover cards displaying title, artist, medium, date, and gallery numbers for image-backed works.

---
