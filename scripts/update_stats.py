"""Generate profile cards from GitHub's public API; no dependencies required."""
import json
import os
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def github(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GH_TOKEN']}"
    with urlopen(Request(f"https://api.github.com{path}", headers=headers), timeout=30) as response:
        return json.load(response)


def collect(username, fetch=github):
    user_path = f"/users/{quote(username, safe='')}"
    user = fetch(user_path)
    repos = []
    page = 1
    while True:
        batch = fetch(f"{user_path}/repos?type=owner&per_page=100&page={page}")
        repos.extend(r for r in batch if not r["fork"] and not r["private"])
        if len(batch) < 100:
            break
        page += 1
    languages = Counter()
    for repo in repos:
        languages.update(fetch(f"/repos/{repo['full_name']}/languages"))
    return dict(repositories=len(repos), followers=user["followers"],
                stars=sum(r["stargazers_count"] for r in repos),
                forks=sum(r["forks_count"] for r in repos), languages=languages)


def card(title, body, updated):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="300" viewBox="0 0 460 300" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">Owned public repositories, excluding forks. Updated {escape(updated)}.</desc>
<style>text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; fill: #e2e8f0; }} .muted {{ fill: #94a3b8; font-size: 12px; }} .label {{ font-size: 14px; }} .value {{ font-size: 25px; font-weight: 700; }}</style>
<rect x="1" y="1" width="458" height="298" rx="16" fill="#0f172a" stroke="#334155"/>
<text x="24" y="36" font-size="19" font-weight="700">{escape(title)}</text>
{body}
<text x="24" y="258" class="muted">Public repositories · forks excluded</text>
<text x="24" y="280" class="muted">Updated {escape(updated)}</text>
</svg>
'''


def render(stats, updated):
    overview = []
    metrics = [("repositories", "Repositories"), ("stars", "Stars received"),
               ("forks", "Forks received"), ("followers", "Followers")]
    for index, (key, label) in enumerate(metrics):
        x, y = 24 + (index % 2) * 220, 92 + (index // 2) * 85
        overview.append(f'<text x="{x}" y="{y}" class="value">{stats[key]:,}</text>')
        overview.append(f'<text x="{x}" y="{y + 25}" class="label">{label}</text>')
    languages = stats["languages"]
    total = sum(languages.values())
    rows = sorted(languages.items(), key=lambda item: (-item[1], item[0]))[:5]
    body = []
    colors = ["#38bdf8", "#a78bfa", "#34d399", "#fbbf24", "#fb7185"]
    for index, (name, size) in enumerate(rows):
        y = 70 + index * 35
        percent = size / total * 100 if total else 0
        body.append(f'<text x="24" y="{y}" class="label">{escape(name)}</text>')
        body.append(f'<text x="436" y="{y}" text-anchor="end" class="muted">{percent:.1f}%</text>')
        body.append(f'<rect x="24" y="{y + 7}" width="412" height="5" rx="2" fill="#334155"/>')
        body.append(f'<rect x="24" y="{y + 7}" width="{412 * percent / 100:.2f}" height="5" rx="2" fill="{colors[index]}"/>')
    if not rows:
        body.append('<text x="24" y="100" class="label">No language data available yet.</text>')
    return {"github-overview.svg": card("GitHub Overview", "\n".join(overview), updated),
            "github-languages.svg": card("Top Languages · Code Bytes", "\n".join(body), updated)}


def main():
    # Complete all API requests before writing, preserving cards on API failure.
    stats = collect(os.environ.get("PROFILE_USERNAME", "Valerie6048"))
    cards = render(stats, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
    output = ROOT / "assets"
    output.mkdir(exist_ok=True)
    for name, contents in cards.items():
        (output / name).write_text(contents, encoding="utf-8")
    print(f"Generated {len(cards)} cards from {stats['repositories']} public repositories.")


if __name__ == "__main__":
    main()
