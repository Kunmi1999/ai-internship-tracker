import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
JOBS_PATH = BASE_DIR / "jobs.json"
README_PATH = BASE_DIR / "README.md"
INDEX_PATH = BASE_DIR / "index.html"


def generate_readme():
    raw_json = JOBS_PATH.read_text(encoding="utf-8")
    data = json.loads(raw_json)
    jobs = data.get("jobs", [])
    meta = data.get("metadata", {})
    last_updated = meta.get("last_updated", "")[:10]

    zero_visa = [j for j in jobs if j["feasibility"].startswith("Zero")]
    high_visa = [j for j in jobs if j["feasibility"].startswith("High")]
    med_visa = [j for j in jobs if j["feasibility"].startswith("Medium")]

    lines = [
        "# 🚀 Summer 2027 AI Product & Business Analyst Internship Radar",
        "",
        f"> **Last Automated Sync:** `{last_updated}` (Runs daily at **8:00 AM CAT / Africa/Kigali** via Antigravity Scheduled Automation)",
        ">",
        f"> **Candidate Profile:** `{meta.get('candidate_profile', '')}`",
        "",
        "## 🌐 Live Interactive Dashboard (GitHub Pages)",
        "- **Live Site:** **[https://kunmi1999.github.io/ai-internship-tracker/](https://kunmi1999.github.io/ai-internship-tracker/)**"
        " *(or open [`index.html`](./index.html) locally)*",
        "",
        "---",
        "",
        "## 🟢 Tier 1: Zero Travel Visa Friction (Kigali, Lagos, Nairobi & Global Remote EOR)",
        "",
        "| Company | Role | Category | Paid / Compensation | Mode & Location | Nigerian + Kigali Residency Path | Application Link |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for j in zero_visa:
        comp = j.get("compensation", j.get("paid_status", "Paid"))
        lines.append(
            f"| **{j['company']}** | {j['title']} | `{j['category']}` | 💰 **{comp}** | {j['work_mode']} ({j['location']}) | {j['nigerian_kigali_visa_path']} | [Apply Here ↗]({j['url']}) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 🔵 Tier 2: High Visa Feasibility (Sponsors J-1 / UK GAE / Schengen via Kigali Embassies)",
        "",
        "| Company | Role | Category | Paid / Compensation | Mode & Location | Nigerian + Kigali Residency Path | Application Link |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ])

    for j in high_visa:
        comp = j.get("compensation", j.get("paid_status", "Paid"))
        lines.append(
            f"| **{j['company']}** | {j['title']} | `{j['category']}` | 💰 **{comp}** | {j['work_mode']} ({j['location']}) | {j['nigerian_kigali_visa_path']} | [Apply Here ↗]({j['url']}) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 🟡 Tier 3: Medium Feasibility (Verify J-1 / Regional Hub Eligibility)",
        "",
        "| Company | Role | Category | Paid / Compensation | Mode & Location | Nigerian + Kigali Residency Path | Application Link |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ])

    for j in med_visa:
        comp = j.get("compensation", j.get("paid_status", "Paid"))
        lines.append(
            f"| **{j['company']}** | {j['title']} | `{j['category']}` | 💰 **{comp}** | {j['work_mode']} ({j['location']}) | {j['nigerian_kigali_visa_path']} | [Apply Here ↗]({j['url']}) |"
        )

    filtered_out = meta.get("filtered_out_examples", [])
    if filtered_out:
        lines.extend([
            "",
            "---",
            "",
            "## 🚫 Automatically Filtered Out (Ineligible Citizenship / Security Clearance)",
            "",
            "| Company | Role | Reason Excluded |",
            "| :--- | :--- | :--- |",
        ])
        for f in filtered_out:
            lines.append(f"| {f['company']} | {f['role']} | {f['reason']} |")

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
