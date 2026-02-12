import sys
import json
from datetime import datetime

#!/usr/bin/env python3
"""
Simple portfolio generator.
Run: python Untitled-1.py [data.json]
If no JSON provided, sample data is used. Writes 'portfolio.html' in current directory.
"""


SAMPLE = {
    "name": "Your Name",
    "title": "Software Engineer",
    "bio": "I build reliable, maintainable software. Open to collaborations and interesting problems.",
    "email": "you@example.com",
    "location": "City, Country",
    "social": {
        "GitHub": "https://github.com/username",
        "LinkedIn": "https://linkedin.com/in/username",
        "Twitter": "https://twitter.com/username"
    },
    "projects": [
        {
            "title": "Project One",
            "description": "Short description of project one. Main tech: Python, Flask.",
            "link": "https://github.com/username/project-one",
            "image": "https://via.placeholder.com/600x300.png?text=Project+One"
        },
        {
            "title": "Project Two",
            "description": "Short description of project two. Main tech: React, TypeScript.",
            "link": "https://github.com/username/project-two",
            "image": "https://via.placeholder.com/600x300.png?text=Project+Two"
        }
    ]
}

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{name} — Portfolio</title>
<style>
:root{{font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,'Helvetica Neue',Arial; color:#111; background:#f7f7fb;}}
body{{max-width:1000px;margin:36px auto;padding:24px;background:#fff;border-radius:12px;box-shadow:0 6px 30px rgba(12,12,20,0.06)}}
header{{display:flex;align-items:center;gap:16px}}
.avatar{{width:96px;height:96px;border-radius:12px;background:#e6e9ef;display:inline-block}}
h1{{margin:0;font-size:1.6rem}}
h2.title{{margin:4px 0 12px;font-weight:500;color:#3b3e4a}}
.bio{{margin:12px 0;color:#555;line-height:1.5}}
.meta{{display:flex;gap:12px;flex-wrap:wrap;color:#6b7082;font-size:0.95rem}}
.projects{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin-top:20px}}
.card{{background:#fff;border:1px solid #eef0f6;border-radius:10px;overflow:hidden;box-shadow:0 4px 20px rgba(11,14,25,0.03)}}
.card img{{width:100%;height:140px;object-fit:cover;display:block}}
.card .pad{{padding:14px}}
.card h3{{margin:0 0 8px;font-size:1.05rem}}
.card p{{margin:0 0 12px;color:#555;font-size:0.95rem}}
.card a.btn{{display:inline-block;padding:8px 12px;background:#2563eb;color:#fff;border-radius:8px;text-decoration:none;font-size:0.95rem}}
footer{{margin-top:28px;color:#8b8f9b;font-size:0.9rem;text-align:center}}
@media (max-width:520px){{body{{margin:12px}} .avatar{{width:72px;height:72px}}}}
</style>
</head>
<body>
<header>
<div class="avatar" aria-hidden></div>
<div>
  <h1>{name}</h1>
  <div class="title">{title}</div>
  <div class="bio">{bio}</div>
  <div class="meta">
    <div>📍 {location}</div>
    <div>✉️ <a href="mailto:{email}">{email}</a></div>
    {social_html}
  </div>
</div>
</header>

<section class="projects">
{projects_html}
</section>

<footer>Generated {year} • Portfolio</footer>
</body>
</html>
"""

PROJECT_CARD = """<article class="card">
  <img src="{image}" alt="{title}">
  <div class="pad">
    <h3>{title}</h3>
    <p>{description}</p>
    <a class="btn" href="{link}" target="_blank" rel="noopener">View project</a>
  </div>
</article>"""

def load_data(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Could not load {path}: {e}")
        sys.exit(1)

def build_social_html(social):
    if not social:
        return ""
    parts = []
    for name, url in social.items():
        parts.append(f'<div><a href="{url}" target="_blank" rel="noopener">{name}</a></div>')
    return "\n    ".join(parts)

def build_projects_html(projects):
    out = []
    for p in projects:
        out.append(PROJECT_CARD.format(
            title=escape(p.get("title","Untitled")),
            description=escape(p.get("description","")),
            link=escape(p.get("link","#")),
            image=escape(p.get("image","https://via.placeholder.com/600x300.png?text=Project"))
        ))
    return "\n".join(out)

def escape(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def main():
    data = SAMPLE
    if len(sys.argv) > 1:
        data = load_data(sys.argv[1])
    html = HTML_TEMPLATE.format(
        name=escape(data.get("name","")),
        title=escape(data.get("title","")),
        bio=escape(data.get("bio","")),
        email=escape(data.get("email","")),
        location=escape(data.get("location","")),
        social_html=build_social_html(data.get("social",{})),
        projects_html=build_projects_html(data.get("projects",[])),
        year=datetime.now().year
    )
    out_path = "portfolio.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Written {out_path}")

if __name__ == "__main__":
    main()