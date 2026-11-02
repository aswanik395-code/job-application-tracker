# Obstacle Log


| # | Obstacle | Solution |
|---|----------|----------|
| 1 | Searching for `"interview"` returned nothing because statuses are stored as `"Interview"`. | Added `_normalize_status()` for case-insensitive matching that returns the canonical name. |
| 2 | Typos like `"Offerd"` silently created bad data and broke summary counts (KeyError). | `_normalize_status()` raises a clear `ValueError` listing valid statuses. |
| 3 | The summary assumed exactly one Interview entry, but several can be active at once. | Summary returns a list of (company, role) pairs and handles the empty case. |
| 4 | Company search failed on partial input (`"goo"` vs `"Google"`). | Used lowercase substring matching. |
| 5 | Updating by company alone is ambiguous if you apply to two roles at one company. | `update_status()` matches on company **and** role. |
| 6 | Data vanished between runs. | Saved to `applications.json` and loaded on startup, with sample data as first-run fallback. |
