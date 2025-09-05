# app.py
from flask import Flask, jsonify, request, abort
import json
from pathlib import Path
from typing import List, Dict
from collections import Counter

DATA_PATH = Path(__file__).parent / "data" / "festivals.json"

def load_data() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

FESTIVALS = load_data()
FESTIVAL_INDEX = {f["id"]: f for f in FESTIVALS}

app = Flask(__name__)

def filter_by_region_month(festivals, region=None, month=None):
    results = festivals
    if region:
        region_lower = region.strip().lower()
        results = [f for f in results if region_lower in f["region"].lower() or region_lower in f.get("location","").lower()]
    if month:
        try:
            m = int(month)
            results = [f for f in results if m in f.get("months", [])]
        except ValueError:
            return []
    return results

@app.route("/festivals", methods=["GET"])
def get_festivals():
    region = request.args.get("region")
    month = request.args.get("month")
    results = filter_by_region_month(FESTIVALS, region=region, month=month)
    # minimal projection for listing
    projection = [
        {
            "id": f["id"],
            "name": f["name"],
            "region": f["region"],
            "location": f.get("location",""),
            "months": f.get("months", []),
            "tags": f.get("tags", [])
        } for f in results
    ]
    return jsonify({"count": len(projection), "results": projection})

@app.route("/festivals/<int:fest_id>", methods=["GET"])
def get_festival(fest_id):
    f = FESTIVAL_INDEX.get(fest_id)
    if not f:
        abort(404, description="Festival not found")
    return jsonify(f)

def tag_similarity(a: List[str], b: List[str]) -> int:
    # simple overlap count
    return len(set([t.lower() for t in a]) & set([t.lower() for t in b]))

@app.route("/recommend", methods=["GET"])
def recommend():
    fid = request.args.get("festival_id", type=int)
    if not fid or fid not in FESTIVAL_INDEX:
        abort(400, description="festival_id is required and must exist")
    source = FESTIVAL_INDEX[fid]
    candidates = [f for f in FESTIVALS if f["id"] != fid]

    # score by tag overlap, then by shared month, then by tag count tie-breaker (popularity not available)
    scored = []
    for c in candidates:
        score = tag_similarity(source.get("tags", []), c.get("tags", []))
        # months overlap increases score
        if set(source.get("months", [])) & set(c.get("months", [])):
            score += 1
        scored.append((score, c))

    scored.sort(key=lambda x: (-x[0], x[1]["name"]))
    top = [ {"id": c["id"], "name": c["name"], "region": c["region"], "tags": c.get("tags", [])} for s,c in scored[:3] ]

    return jsonify({"source_festival": {"id": source["id"], "name": source["name"]}, "recommendations": top})

@app.route("/regions", methods=["GET"])
def regions():
    regions = sorted({f["region"] for f in FESTIVALS})
    return jsonify({"regions": regions})

@app.route("/months", methods=["GET"])
def months():
    months_set = set()
    for f in FESTIVALS:
        months_set.update(f.get("months", []))
    months_list = sorted(months_set)
    return jsonify({"months": months_list})

if __name__ == "__main__":
    app.run(debug=True)
