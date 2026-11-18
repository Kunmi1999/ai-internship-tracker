import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
JOBS_PATH = BASE_DIR / "jobs.json"
README_PATH = BASE_DIR / "README.md"


def generate_readme():
    data = json.loads(JOBS_PATH.read_text(encoding="utf-8"))
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
        "Once GitHub Pages is enabled on this repository (`Settings -> Pages -> Deploy from main branch`), your interactive filterable site is live at:",
        "- **`https://kunmi1999.github.io/ai-internship-tracker/`** *(or open [`index.html`](./index.html) directly)*",
        "",
        "---",
        "",
        "## 🟢 Tier 1: Zero Travel Visa Friction (Kigali, Lagos, Nairobi & Global Remote EOR)",
        "",
        "| Company | Role | Category | Mode & Location | Nigerian + Kigali Residency Path | Apply |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for j in zero_visa:
        lines.append(
            f"| **{j['company']}** | {j['title']} | `{j['category']}` | {j['work_mode']} ({j['location']}) | {j['nigerian_kigali_visa_path']} | [Apply ↗]({j['url']}) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 🔵 Tier 2: High Visa Feasibility (Sponsors J-1 / UK GAE / Schengen via Kigali Embassies)",
        "",
        "| Company | Role | Category | Mode & Location | Nigerian + Kigali Residency Path | Apply |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ])

    for j in high_visa:
        lines.append(
            f"| **{j['company']}** | {j['title']} | `{j['category']}` | {j['work_mode']} ({j['location']}) | {j['nigerian_kigali_visa_path']} | [Apply ↗]({j['url']}) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 🟡 Tier 3: Medium Feasibility (Verify J-1 / Regional Hub Eligibility)",
        "",
        "| Company | Role | Category | Mode & Location | Nigerian + Kigali Residency Path | Apply |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ])

    for j in med_visa:
        lines.append(
            f"| **{j['company']}** | {j['title']} | `{j['category']}` | {j['work_mode']} ({j['location']}) | {j['nigerian_kigali_visa_path']} | [Apply ↗]({j['url']}) |"
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
    print(f"Successfully generated {README_PATH} with {len(jobs)} roles.")


if __name__ == "__main__":
    generate_readme()
