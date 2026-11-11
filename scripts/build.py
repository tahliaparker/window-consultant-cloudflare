import json
import html
import re
import os
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen

OWNER = "tahliaparker"
SOURCE_REPO = "window-consultant"

SITE_NAME = "Window Consultant"
SITE_DESCRIPTION = (
    "Independent notes on window care, glass, "
    "home maintenance, and thoughtful improvements."
)

OUTPUT = Path("dist")
POSTS = OUTPUT / "posts"

TOKEN = os.environ.get("GH_TOKEN", "")


def get_issues():
    issues = []
    page = 1

    while True:
        url = (
            f"https://api.github.com/repos/{OWNER}/"
            f"{SOURCE_REPO}/issues"
            f"?state=open&per_page=100&page={page}"
        )

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "WindowConsultantCloudflare",
        }

        if TOKEN:
            headers["Authorization"] = f"Bearer {TOKEN}"

        request = Request(url, headers=headers)

        with urlopen(request, timeout=30) as response:
            batch = json.load(response)

        issues.extend(
            item for item in batch
            if "pull_request" not in item
        )

        if len(batch) < 100:
            break

        page += 1

    return sorted(
        issues,
        key=lambda item: item["created_at"],
        reverse=True,
    )


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:65] or "article"


def format_content(text):
    text = html.escape(text or "")

    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        lambda match: (
            '<a href="'
            + html.escape(match.group(2), quote=True)
            + '" rel="noopener noreferrer">'
            + match.group(1)
            + "</a>"
        ),
        text,
    )

    paragraphs = re.split(r"\n\s*\n", text)

    return "\n".join(
        "<p>" + p.replace("\n", "<br>") + "</p>"
        for p in paragraphs if p.strip()
    )


CSS = """
:root {
    --background: #f5f4f1;
    --surface: #ffffff;
    --ink: #292d30;
    --muted: #707477;
    --accent: #ad6650;
    --border: #e4e1dc;
}
* {
    box-sizing: border-box;
}
body {
    margin: 0;
    background: var(--background);
    color: var(--ink);
    font-family: Arial, Helvetica, sans-serif;
    line-height: 1.7;
}
a {
    color: var(--accent);
}
.topbar {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
}
.topbar-inner {
    max-width: 1160px;
    margin: auto;
    padding: 26px 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
}
.logo {
    color: var(--ink);
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -1px;
    text-decoration: none;
}
.topbar-label {
    color: var(--accent);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: bold;
}
.intro {
    max-width: 1160px;
    margin: auto;
    padding: 90px 30px 70px;
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 50px;
    align-items: end;
}
.kicker {
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-size: 12px;
    font-weight: bold;
}
.intro h1 {
    font-size: clamp(45px, 6vw, 82px);
    line-height: 1.04;
    letter-spacing: -3px;
    margin: 18px 0 0;
}
.intro p {
    font-size: 19px;
    color: var(--muted);
    max-width: 390px;
}
.content {
    max-width: 1160px;
    margin: 0 auto 100px;
    padding: 0 30px;
}
.section-title {
    padding: 22px 0;
    border-top: 2px solid var(--ink);
    font-size: 13px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.article-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 24px;
}
.article-card {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 38px;
    min-height: 260px;
    display: flex;
    flex-direction: column;
}
.article-card time {
    font-size: 12px;
    color: var(--accent);
    letter-spacing: 1px;
}
.article-card h2 {
    font-size: 29px;
    line-height: 1.25;
    letter-spacing: -0.7px;
    margin: 20px 0;
}
.article-card h2 a {
    color: var(--ink);
    text-decoration: none;
}
.article-card h2 a:hover {
    color: var(--accent);
}
.article-card p {
    color: var(--muted);
    margin: 0 0 25px;
}
.article-card .read-link {
    margin-top: auto;
    text-decoration: none;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 1.5px;
    font-weight: bold;
}
.empty {
    background: var(--surface);
    padding: 65px 30px;
    border: 1px solid var(--border);
    text-align: center;
    color: var(--muted);
}
.article-page {
    max-width: 820px;
    margin: 65px auto 100px;
    padding: 60px;
    background: var(--surface);
    border: 1px solid var(--border);
}
.article-page h1 {
    font-size: clamp(34px, 5vw, 54px);
    line-height: 1.15;
    letter-spacing: -1.5px;
}
.article-page time {
    color: var(--accent);
    font-size: 13px;
}
.article-body {
    margin-top: 40px;
    font-size: 18px;
    overflow-wrap: anywhere;
}
.article-body p {
    margin-bottom: 24px;
}
.back {
    display: inline-block;
    margin-top: 40px;
    text-decoration: none;
    font-size: 13px;
    font-weight: bold;
}
footer {
    background: #292d30;
    color: #e8e5df;
    padding: 40px 30px;
}
.footer-inner {
    max-width: 1160px;
    margin: auto;
    display: flex;
    justify-content: space-between;
    gap: 20px;
    font-size: 13px;
}
@media (max-width: 700px) {
    .topbar-inner {
        padding: 22px;
    }
    .topbar-label {
        display: none;
    }
    .intro {
        display: block;
        padding: 55px 22px;
    }
    .intro h1 {
        letter-spacing: -1.5px;
    }
    .content {
        padding: 0 22px;
    }
    .article-grid {
        grid-template-columns: 1fr;
    }
    .article-card {
        padding: 28px;
    }
    .article-page {
        margin: 20px;
        padding: 28px;
    }
    .footer-inner {
        flex-direction: column;
    }
}
"""


def template(title, content, description=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | {SITE_NAME}</title>
<meta name="description"
content="{html.escape(description, quote=True)}">
<style>{CSS}</style>
</head>
<body>
<header class="topbar">
    <div class="topbar-inner">
        <a class="logo" href="/">{SITE_NAME}</a>
        <span class="topbar-label">The Home Journal</span>
    </div>
</header>
{content}
<footer>
    <div class="footer-inner">
        <span>© {datetime.now(timezone.utc).year}
        {SITE_NAME}. All rights reserved.</span>
        <span>Windows / Glass / Maintenance / Living</span>
    </div>
</footer>
</body>
</html>"""


def main():
    POSTS.mkdir(parents=True, exist_ok=True)

    issues = get_issues()
    cards = []
    active_files = set()

    for issue in issues:
        title = issue.get("title") or "Untitled"
        body = issue.get("body") or ""
        date = issue["created_at"][:10]

        filename = (
            f'{issue["number"]}-{slugify(title)}.html'
        )
        active_files.add(filename)
        link = f"/posts/{filename}"

        article = f"""
<main class="article-page">
    <span class="kicker">Window Consultant / Article</span>
    <h1>{html.escape(title)}</h1>
    <time datetime="{date}">{date}</time>
    <div class="article-body">
        {format_content(body)}
    </div>
    <a class="back" href="/">← Back to articles</a>
</main>
"""

        (POSTS / filename).write_text(
            template(title, article, body[:155]),
            encoding="utf-8",
        )

        summary = re.sub(r"\s+", " ", body).strip()
        excerpt = html.escape(summary[:165])

        if len(summary) > 165:
            excerpt += "..."

        cards.append(f"""
<article class="article-card">
    <time datetime="{date}">{date}</time>
    <h2><a href="{link}">{html.escape(title)}</a></h2>
    <p>{excerpt}</p>
    <a class="read-link" href="{link}">
        Continue Reading →
    </a>
</article>
""")

    for old_file in POSTS.glob("*.html"):
        if old_file.name not in active_files:
            old_file.unlink()

    articles_html = (
        '<div class="article-grid">'
        + "\n".join(cards)
        + "</div>"
        if cards
        else '<div class="empty">New stories are coming soon.</div>'
    )

    homepage = f"""
<section class="intro">
    <div>
        <span class="kicker">Window Consultant Journal</span>
        <h1>Details make<br>the difference.</h1>
    </div>
    <p>{SITE_DESCRIPTION}</p>
</section>
<main class="content">
    <h2 class="section-title">Recent Publications</h2>
    {articles_html}
</main>
"""

    (OUTPUT / "index.html").write_text(
        template(SITE_NAME, homepage, SITE_DESCRIPTION),
        encoding="utf-8",
    )

    (OUTPUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n",
        encoding="utf-8",
    )

    (OUTPUT / "_headers").write_text(
        "/*\n  X-Content-Type-Options: nosniff\n",
        encoding="utf-8",
    )

    print(
        f"Cloudflare build complete: {len(issues)} articles."
    )


if __name__ == "__main__":
    main()
