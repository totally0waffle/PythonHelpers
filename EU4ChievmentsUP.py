import requests
from bs4 import BeautifulSoup
import json
import re
import os

STEAM_API_KEY = "STEAM API KEY GOES HERE"
STEAM_ID = "STEAM ID GOES HERE"
APP_ID = 236850
WIKI_URL = "https://eu4.paradoxwikis.com/Achievements"
LOCAL_WIKI_FILE = "WIKI.html"
OUTPUT_HTML = "eu4_achievement_tracker.html"
DOWNLOAD_WIKI = False

def normalize(text):
    return text.strip().replace("\xa0", " ")

if DOWNLOAD_WIKI and not os.path.exists(LOCAL_WIKI_FILE):
    print("Downloading EU4 wiki page...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    r = requests.get(WIKI_URL, headers=headers)
    with open(LOCAL_WIKI_FILE, "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Wiki page saved locally.")
print("Loading wiki HTML...")

with open(LOCAL_WIKI_FILE, "r", encoding="utf-8") as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")
tables = soup.find_all("table")
achievement_tables = []

for t in tables:
    if "Achievement" in t.text:
        achievement_tables.append(t)

print("Tables detected:", len(achievement_tables))
tables = soup.find_all("table", class_="mildtable")
wiki_data = {}
for table in tables:
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue
        title_div = cols[0].find("div", style=lambda x: x and "font-weight: bold" in x)
        if not title_div:
            continue
        title = normalize(title_div.get_text())
        desc_div = title_div.find_next_sibling("div")
        description = ""
        if desc_div:
            description = desc_div.get_text(strip=True)
        start_conditions = cols[1].get_text(" ", strip=True)
        completion = cols[2].get_text(" ", strip=True)
        notes = cols[3].get_text(" ", strip=True)
        wiki_data[title] = {
            "description": description,
            "start": start_conditions,
            "completion": completion,
            "notes": notes
        }
print("Wiki achievements parsed:", len(wiki_data))
print("Fetching Steam achievements...")

steam_url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={STEAM_API_KEY}&steamid={STEAM_ID}&appid={APP_ID}"
data = requests.get(steam_url).json()
locked = set()
for ach in data["playerstats"]["achievements"]:
    if ach["achieved"] == 0:
        locked.add(ach["apiname"])

schema_url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={STEAM_API_KEY}&appid={APP_ID}"
schema = requests.get(schema_url).json()
steam_lookup = {}
for ach in schema["game"]["availableGameStats"]["achievements"]:
    steam_lookup[ach["name"]] = {
        "title": ach["displayName"],
        "desc": ach.get("description","")
    }
country_map = {}
for api in locked:
    if api not in steam_lookup:
        continue
    title = normalize(steam_lookup[api]["title"])
    desc = steam_lookup[api]["desc"]
    country = "Any Nation"
    tips = ""
    difficulty = ""
    entry = wiki_data.get(title)
    if entry:
        text = entry.get("start", "")
        tips = entry.get("notes", "")
    # detect starting country phrases NEEDS TWEAKING REGEX CURRENTLY BROKEN
        match = re.search(r"(?:Playing|Starting| ) as ([A-Za-z ]+?),*(?=\s(?:Make|Unite|Not|Religion|[A-Za-z]+)|$)", text)
        print(match)
        if match:
            country = match.group(1).strip()
        tips = entry.get("notes", "")
        country_map.setdefault(country, [])
        country_map[country].append({
            "title": title,
            "desc": desc,
            "tips": tips,
            "difficulty": difficulty
        })

countries = sorted(country_map.keys())
html_out = """
<html>
<head>
<title>EU4 Achievement Ledger</title>

<style>
body{
background:#2b2b2b;
color:#e6d8a8;
font-family:Georgia;
}

.container{
width:1000px;
margin:auto;
}

.achievement{
border-bottom:1px solid #555;
padding:10px;
}

.tips{
font-style:italic;
color:#cbbd8a;
}
.dropdown {
  position: relative;
  display: inline-block; /* Allows other elements to sit next to it */
}

.dropbtn {
  background-color: #2b2b2b;
  color: #e6d8a8;
  padding: 16px;
  font-size: 16px;
  border: none;
  cursor: pointer;
}

.dropdown-content {
  display: none; /* Initially hide the content */
  position: absolute;
  background-color: #2b2b2b;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content button {
  color: #e6d8a8;
  padding: 12px 16px;
  text-decoration: none;
  display: block; /* Make buttons stack vertically */
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.dropdown-content button:hover {
  background-color: #2b2b2b;
}

.dropdown:hover .dropdown-content {
  display: block; /* Show content on hover */
}

.dropdown:hover .dropbtn {
  background-color: #3e8e41;
}
</style>

<script>
function filterCountry(country){

var sections=document.getElementsByClassName("country-section")

for(let s of sections){

if(country=="All" || s.dataset.country==country){
s.style.display="block"
}else{
s.style.display="none"
}

}

}
</script>

</head>

<body>

<div class="container">

<h1>EU4 Achievement Ledger</h1>
<div class="dropdown">
<button class="dropbtn"> Country Filter</button>
<div class="dropdown-content">
<button onclick="filterCountry('All')">All</button>
"""
print(countries)
for c in countries:
    html_out += f"<button onclick=\"filterCountry('{c}')\">{c}</button>"

html_out +="</div></div>"
for country in countries:
    html_out += f'<div class="country-section" data-country="{country}">'
    html_out += f"<h2>{country}</h2>"

    for ach in country_map[country]:
        html_out += f"""
        <div class="achievement">
        <b>{ach['title']}</b> ({ach['difficulty']})<br>
        {ach['desc']}
        <div class="tips">{ach['tips']}</div>
        </div>
        """

    html_out += "</div>"
html_out += "</div></body></html>"

with open(OUTPUT_HTML,"w",encoding="utf8") as f:
    f.write(html_out)

print("HTML generated:", OUTPUT_HTML)
