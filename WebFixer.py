from bs4 import BeautifulSoup
from pathlib import Path

# ================= CONFIG =================

OLD_DOMAIN = ""   # ENTER OLD URL HERE
NEW_DOMAIN = ""   # "" = relative paths
SITE_ROOT = Path(".")   # RUN IN ROOT DIRECTORY OF WEBPAGE OTHERWISE CHANGE THIS VALUE

missing_assets = []
removed_wp_scripts = set()

def normalize_url(url):
    if not url:
        return url
    if url.startswith(("#", "mailto:", "tel:", "javascript:")):
        return url
    if OLD_DOMAIN in url:
        url = url.replace(OLD_DOMAIN, NEW_DOMAIN)
    if url.startswith("/"):
        url = url[1:]
    return url

def asset_exists(url):
    clean = url.split("?")[0].split("#")[0]
    return (SITE_ROOT / clean).exists()

def enforce_script_order(soup):
    jquery = []
    jquery_ui = []
    others = []
    for script in soup.find_all("script"):
        src = script.get("src", "")
        if "jquery" in src and "ui" not in src:
            jquery.append(script)
        elif "jquery-ui" in src or "effects" in src:
            jquery_ui.append(script)
        else:
            others.append(script)
    for s in soup.find_all("script"):
        s.extract()
    body = soup.body or soup
    for s in jquery + jquery_ui + others:
        body.append(s)

for html_file in SITE_ROOT.rglob("*.html"):
    soup = BeautifulSoup(
        html_file.read_text(encoding="utf-8", errors="ignore"),
        "lxml"
    )
    for tag in soup.find_all(["script", "link", "img"]):
        attr = "src" if tag.name != "link" else "href"
        url = tag.get(attr)
        if not url:
            continue
        if any(x in url for x in ["admin-ajax.php", "wp-json"]):
            removed_wp_scripts.add(url)
            tag.decompose()
            continue
        if "wp-includes/js/imagesloaded.min.js" in url:
            tag[attr] = (
                "https://cdnjs.cloudflare.com/ajax/libs/"
                "jquery.imagesloaded/4.1.4/imagesloaded.pkgd.min.js"
            )
            continue
        new_url = normalize_url(url)
        tag[attr] = new_url
        if tag.name != "script" or not new_url.startswith("http"):
            if not asset_exists(new_url):
                missing_assets.append((html_file, new_url))
    enforce_script_order(soup)
    html_file.write_text(str(soup), encoding="utf-8")

# ================= REPORT =================

print("\n=== STATIC FIX REPORT ===\n")

if missing_assets:
    print("❌ Missing Assets:")
    for page, asset in missing_assets:
        print(f"- {page}: {asset}")
else:
    print("✅ No missing local assets detected.")
if removed_wp_scripts:
    print("\n⚠️ Removed WordPress-only scripts:")
    for s in removed_wp_scripts:
        print(f"- {s}")
print("\n✅ Fixing complete.")