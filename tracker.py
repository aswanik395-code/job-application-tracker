"""Personal Job Application Tracker.

Run:  python tracker.py
Creates/uses applications.json and writes tracker_report.txt.
"""
import json
import os
from datetime import date

DATA_FILE = "applications.json"
REPORT_FILE = "tracker_report.txt"
STATUSES = ["Applied", "Interview", "Selected", "Rejected"]

# ---------- Step 1: sample data ----------
SAMPLE_APPLICATIONS = [
    {"company": "Google",   "role": "Backend Engineer",    "status": "Interview", "date": "2026-09-05"},
    {"company": "Infosys",  "role": "Python Developer",    "status": "Applied",   "date": "2026-09-12"},
    {"company": "Zoho",     "role": "Software Engineer",   "status": "Selected",  "date": "2026-08-28"},
    {"company": "Amazon",   "role": "SDE I",               "status": "Rejected",  "date": "2026-08-15"},
    {"company": "Razorpay", "role": "Data Analyst",        "status": "Applied",   "date": "2026-10-01"},
    {"company": "Flipkart", "role": "Full Stack Developer","status": "Interview", "date": "2026-09-20"},
    {"company": "TCS",      "role": "Systems Engineer",    "status": "Rejected",  "date": "2026-08-10"},
    {"company": "Freshworks","role": "QA Automation Engineer","status": "Applied","date": "2026-10-18"},
]


# ---------- Storage helpers ----------
def load_applications(path=DATA_FILE):
    """Load applications from JSON; fall back to sample data on first run."""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return [dict(app) for app in SAMPLE_APPLICATIONS]


def save_applications(apps, path=DATA_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=2)


def _normalize_status(status):
    """Match a status case-insensitively; raise if it's not a valid stage."""
    for valid in STATUSES:
        if valid.lower() == status.strip().lower():
            return valid
    raise ValueError(f"Invalid status '{status}'. Choose from: {', '.join(STATUSES)}")


# ---------- Step 2: core functions ----------
def add_application(apps, company, role, status="Applied", applied_on=None):
    """Add a new application and return it (None if it already exists)."""
    for a in apps:
        if a["company"].lower() == company.strip().lower() and a["role"].lower() == role.strip().lower():
            print(f"Already tracked: {company} - {role}. Skipping.")
            return None
    app = {
        "company": company.strip(),
        "role": role.strip(),
        "status": _normalize_status(status),
        "date": applied_on or date.today().isoformat(),
    }
    apps.append(app)
    return app


def search_by_status(apps, status):
    status = _normalize_status(status)
    return [a for a in apps if a["status"] == status]


def search_by_company(apps, company):
    """Case-insensitive partial match, e.g. 'goo' finds Google."""
    term = company.strip().lower()
    return [a for a in apps if term in a["company"].lower()]


def update_status(apps, company, role, new_status):
    """Update one application's status. Returns True if found."""
    new_status = _normalize_status(new_status)
    for a in apps:
        if a["company"].lower() == company.lower() and a["role"].lower() == role.lower():
            a["status"] = new_status
            return True
    return False


# ---------- Step 3: summary ----------
def summarize(apps):
    counts = {s: 0 for s in STATUSES}
    for a in apps:
        counts[a["status"]] += 1
    interviews = [(a["company"], a["role"]) for a in apps if a["status"] == "Interview"]
    return {"total": len(apps), "counts": counts, "interviews": interviews}


def format_summary(summary):
    lines = [f"Total applications: {summary['total']}", "", "Applications per status:"]
    for status, n in summary["counts"].items():
        lines.append(f"  {status:<10} {n}")
    lines += ["", "Currently at Interview stage:"]
    if summary["interviews"]:
        lines += [f"  - {c} — {r}" for c, r in summary["interviews"]]
    else:
        lines.append("  (none)")
    return "\n".join(lines)


# ---------- Step 4: save report ----------
def save_report(apps, path=REPORT_FILE):
    lines = ["JOB APPLICATION TRACKER REPORT",
             f"Generated: {date.today().isoformat()}",
             "=" * 60, "", "ALL APPLICATIONS", "-" * 60,
             f"{'Company':<14}{'Role':<26}{'Status':<11}{'Date'}"]
    for a in sorted(apps, key=lambda x: x["date"]):
        lines.append(f"{a['company']:<14}{a['role']:<26}{a['status']:<11}{a['date']}")
    lines += ["", "SUMMARY", "-" * 60, format_summary(summarize(apps)), ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ---------- Demo ----------
def main():
    apps = load_applications()

    print("Adding a new application...")
    add_application(apps, "Swiggy", "Backend Developer", "applied", "2026-10-28")

    print("Updating Infosys: Applied -> Interview")
    update_status(apps, "Infosys", "Python Developer", "interview")

    print("\nSearch by status 'Interview':")
    for a in search_by_status(apps, "Interview"):
        print(f"  {a['company']} - {a['role']}")

    print("\nSearch by company 'zo':")
    for a in search_by_company(apps, "zo"):
        print(f"  {a['company']} - {a['role']} ({a['status']})")

    print("\n" + format_summary(summarize(apps)))

    save_applications(apps)
    save_report(apps)
    print(f"\nSaved {DATA_FILE} and {REPORT_FILE}")


if __name__ == "__main__":
    main()