import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
JOBS_PATH = BASE_DIR / "jobs.json"
README_PATH = BASE_DIR / "README.md"
INDEX_PATH = BASE_DIR / "index.html"


def short_pay(job):
    c = job.get("compensation") or job.get("paid_status") or "Paid"
    c = re.sub(r"^Paid\s*\(", "", c, flags=re.IGNORECASE)
    return c.rstrip(")")


def short_visa(job):
    f = job.get("feasibility", "")
    loc = (job.get("location", "") + " " + job.get("region", "")).lower()
    if f.startswith("Zero"):
        if job.get("work_mode") == "Remote":
            return "🟢 **No Visa Needed** (Remote from Kigali/Nigeria)"
        return "🟢 **Zero Visa** (Rwanda Permit / Nigerian Citizen)"
    if any(k in loc for k in ["uk", "london", "united kingdom", "glasgow"]):
        prefix = "🔵 **UK GAE Visa (Sponsored)**" if f.startswith("High") else "🟡 **Verify UK GAE**"
        return f"{prefix} via VFS Kigali"
    if any(k in loc for k in ["france", "paris", "germany", "berlin", "munich", "amsterdam", "zurich", "schengen"]):
        return "🔵 **Schengen Student Permit** (CMU Agreement via Kigali Embassy)"
    if any(k in loc for k in ["usa", "united states", "san francisco", "california", "palo alto", "santa clara", "pleasanton"]):
        prefix = "🔵 **US J-1 Intern (Sponsored)**" if f.startswith("High") else "🟡 **Verify US J-1**"
        return f"{prefix} via U.S. Embassy Kigali"
    return "🔵 **Visa Sponsored** (Apply from Kigali)"


def generate_readme():
    raw_json = JOBS_PATH.read_text(encoding="utf-8")
    data = json.loads(raw_json)
    jobs = data.get("jobs", [])
    meta = data.get("metadata", {})
    last_updated = meta.get("last_updated", "")[:10]

    lines = [
        "# Summer 2027 AI Internship Tracker (At a Glance)",
        "",
        f"**Last Synced:** `{last_updated}` • **Total Paid Roles:** `{len(jobs)}` • **Dashboard & 1-Page CV Generator:** Open [`index.html`](./index.html)",
        "",
        "| Company & Role | Track | Location & Mode | Pay | Your Visa Path (Nigerian in Kigali) | Apply |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for j in jobs:
        lines.append(
            f"| **{j['company']}** — {j['title']} | `{j['category']}` | {j['location']} ({j['work_mode']}) | 💰 {short_pay(j)} | {short_visa(j)} | [Apply ↗]({j['url']}) |"
        )

    lines.append("")
    README_PATH.write_text("\n".join(lines), encoding="utf-8")

    if INDEX_PATH.exists():
        html = INDEX_PATH.read_text(encoding="utf-8")
        replacement = f"/* FALLBACK_DATA_START */\n    const FALLBACK_DATA = {raw_json.strip()};\n    /* FALLBACK_DATA_END */"
        html = re.sub(
            r"/\* FALLBACK_DATA_START \*/.*?/\* FALLBACK_DATA_END \*/",
            lambda _: replacement,
            html,
            flags=re.DOTALL,
        )
        INDEX_PATH.write_text(html, encoding="utf-8")

    print(f"Successfully synced {README_PATH} and {INDEX_PATH} with {len(jobs)} roles.")


if __name__ == "__main__":
    generate_readme()
