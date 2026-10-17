from pathlib import Path
import time
import pandas as pd
import requests

DATA_DIR = Path("/Users/destinybrewington/PycharmProjects/Met_Female_Modern_Art")
AUDIT_CSV = DATA_DIR / "met_modern_art.csv"
OUTPUT_NUDES_CSV = DATA_DIR / "art_images.csv"

df = pd.read_csv(AUDIT_CSV, low_memory=False)
nudes_df = df[df["Is_Nude"] == True].copy()
print(f"Querying image assets for {len(nudes_df)} nude artworks...")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "application/json",
})

thumb_urls = []
for idx, obj_id in enumerate(nudes_df["Object ID"], start=1):
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
    img = ""
    try:
        r = session.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            img = data.get("primaryImageSmall", "") or data.get("primaryImage", "")
            if not img:
                add_imgs = data.get("additionalImages", []) or []
                if add_imgs:
                    img = add_imgs[0]
    except Exception as e:
        pass

    thumb_urls.append(img)
    time.sleep(0.04)

nudes_df["primaryImageSmall"] = thumb_urls
nudes_df.to_csv(OUTPUT_NUDES_CSV, index=False)

valid_count = sum(1 for u in thumb_urls if str(u).startswith("http"))
print(f"Finished: {valid_count} photos resolved. Saved to {OUTPUT_NUDES_CSV}")