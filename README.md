# Festival Finder API

**Festival Finder** is a simple Flask-based JSON API that returns information about Filipino festivals by region or month. It also includes a unique recommendation feature that suggests similar or lesser-known festivals based on theme tags — useful for discovering alternative local celebrations.

---

## Features

- `GET /festivals` — search festivals by `region` (string) and/or `month` (1–12). Returns matching festivals in JSON.
- `GET /festivals/<id>` — get detailed festival data by ID.
- `GET /recommend?festival_id=<id>` — **unique feature**: returns 3 recommended festivals that share similar tags or themes. Helps discover lesser-known festivals similar to a popular one.
- `GET /regions` — list available regions in dataset.
- `GET /months` — list months that have festivals in dataset.

The API is intentionally file-based (simple JSON data) so collaborators can easily edit festival entries and extend features.

---

## Dataset

The repo contains a `data/festivals.json` file with ~20–25 curated Filipino festivals. Each entry includes:

```json
{
  "id": 1,
  "name": "Sinulog Festival",
  "region": "Central Visayas",
  "location": "Cebu City, Cebu",
  "months": [1],
  "date_notes": "Third Sunday of January",
  "tags": ["religious", "dance", "street parade"],
  "description": "A grand street parade honoring the Santo Niño with ranks of dancers and drums."
}
