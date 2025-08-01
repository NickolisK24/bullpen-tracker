from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import csv
from datetime import datetime
import logging
from werkzeug.utils import secure_filename
import traceback

from pitcher import Pitcher
from fatigue_utils import fatigue_color

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = Flask(__name__)

# CORS: allow origin from environment or fallback to localhost frontend default
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
CORS(app, origins=[frontend_origin])

# Directory / file constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_FILENAME = "game_logs.csv"
CSV_PATH = os.path.join(DATA_DIR, CSV_FILENAME)

REQUIRED_COLUMNS = {"name", "team", "handedness", "date", "pitch_count"}
ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def load_pitchers():
    """
    Load pitchers from the CSV. Returns (pitchers_dict, errors_list).
    """
    pitchers = {}
    errors = []

    if not os.path.exists(CSV_PATH):
        logging.info("CSV file not found; returning empty pitcher list.")
        return pitchers, errors

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header_cols = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - header_cols
        if missing:
            msg = f"CSV is missing required columns: {sorted(list(missing))}"
            logging.warning(msg)
            errors.append(msg)
            return pitchers, errors

        for idx, row in enumerate(reader, start=1):
            name = (row.get("name") or "").strip()
            team = (row.get("team") or "").strip()
            handedness = (row.get("handedness") or "").strip()
            date_str = (row.get("date") or "").strip()
            pitch_count_raw = (row.get("pitch_count") or "").strip()

            if not (name and team and handedness and date_str and pitch_count_raw):
                logging.warning("Row %s skipped for missing field(s): %s", idx, row)
                continue

            try:
                pitch_count = int(pitch_count_raw)
            except ValueError:
                logging.warning("Row %s has invalid pitch_count '%s'; skipping.", idx, pitch_count_raw)
                continue

            try:
                if name not in pitchers:
                    pitchers[name] = Pitcher(name, team, handedness)
                else:
                    if not getattr(pitchers[name], "handedness", "") and handedness:
                        pitchers[name].handedness = handedness
                pitchers[name].add_game(date_str, pitch_count)
            except Exception as e:
                logging.warning("Row %s error parsing/adding game: %s; skipping.", idx, e)
                continue

    return pitchers, errors


@app.route("/")
def index():
    return jsonify({
        "message": "Bullpen Buddy backend is running. Use /api/health, /api/pitchers, etc."
    }), 200


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/pitchers", methods=["GET"])
def get_pitchers():
    """
    Returns all pitchers with fatigue and status.
    Supports query params:
      - team (substring, case-insensitive)
      - min_fatigue / max_fatigue (numeric)
      - sort: fatigue | name | team (default: fatigue)
      - order: asc | desc (default: desc)
      - limit: integer
    """
    pitchers, errors = load_pitchers()
    if errors:
        return jsonify({"errors": errors, "data": []}), 400

    today = datetime.today()
    results = []
    for p in pitchers.values():
        fatigue = p.calculate_fatigue(today)
        results.append({
            "name": p.name,
            "team": p.team,
            "handedness": getattr(p, "handedness", ""),
            "fatigue": fatigue,
            "status": fatigue_color(fatigue)
        })

    # Filtering
    team_filter = request.args.get("team", "").strip().lower()
    if team_filter:
        results = [r for r in results if team_filter in r["team"].lower()]

    try:
        min_f = float(request.args.get("min_fatigue")) if request.args.get("min_fatigue") else None
    except ValueError:
        return jsonify({"error": "min_fatigue must be numeric"}), 400
    try:
        max_f = float(request.args.get("max_fatigue")) if request.args.get("max_fatigue") else None
    except ValueError:
        return jsonify({"error": "max_fatigue must be numeric"}), 400

    if min_f is not None:
        results = [r for r in results if r["fatigue"] >= min_f]
    if max_f is not None:
        results = [r for r in results if r["fatigue"] <= max_f]

    # Sorting
    sort_key = request.args.get("sort", "fatigue")
    if sort_key not in {"fatigue", "name", "team"}:
        return jsonify({"error": "sort must be one of 'fatigue', 'name', or 'team'"}), 400
    reverse = True if request.args.get("order", "desc").lower() == "desc" else False
    results = sorted(results, key=lambda x: x[sort_key], reverse=reverse)

    # Limit
    if request.args.get("limit"):
        try:
            limit = int(request.args.get("limit"))
            if limit >= 0:
                results = results[:limit]
        except ValueError:
            return jsonify({"error": "limit must be an integer"}), 400

    return jsonify(results), 200


@app.route("/api/pitchers/<string:normalized_name>", methods=["GET"])
def get_pitcher_by_name(normalized_name):
    pitchers, errors = load_pitchers()
    if errors:
        return jsonify({"errors": errors}), 400

    today = datetime.today()
    # case-insensitive exact match
    for p in pitchers.values():
        if p.name.lower() == normalized_name.lower():
            fatigue = p.calculate_fatigue(today)
            return jsonify({
                "name": p.name,
                "team": p.team,
                "handedness": getattr(p, "handedness", ""),
                "fatigue": fatigue,
                "status": fatigue_color(fatigue)
            }), 200

    return jsonify({"error": f"Pitcher '{normalized_name}' not found"}), 404


@app.route("/api/upload", methods=["POST"])
def upload_csv():
    try:
        logging.info(
            "Upload request received. Origin: %s | Files: %s | Form keys: %s",
            request.headers.get("Origin"),
            list(request.files.keys()),
            list(request.form.keys()),
        )

        if "file" not in request.files:
            logging.warning("Upload attempt without 'file' part. Keys: %s", list(request.files.keys()))
            return jsonify({"error": "No file part in request"}), 400

        file = request.files["file"]
        if file.filename == "":
            logging.warning("Upload attempt with empty filename.")
            return jsonify({"error": "No selected file"}), 400

        if not allowed_file(file.filename):
            logging.warning("Upload attempt with disallowed filename: %s", file.filename)
            return jsonify({"error": "Only CSV files are allowed"}), 400

        filename = secure_filename(file.filename)
        os.makedirs(DATA_DIR, exist_ok=True)
        save_path = os.path.join(DATA_DIR, CSV_FILENAME)

        file.save(save_path)

        exists = os.path.exists(save_path)
        size = os.path.getsize(save_path) if exists else 0
        dir_contents = os.listdir(DATA_DIR)

        logging.info(
            "CSV uploaded and saved to %s (original: %s). exists=%s size=%s contents=%s",
            save_path,
            filename,
            exists,
            size,
            dir_contents,
        )

        return jsonify({
            "message": "File uploaded successfully",
            "debug": {
                "saved_as": CSV_FILENAME,
                "exists": exists,
                "size_bytes": size,
                "data_dir_contents": dir_contents
            }
        }), 200

    except Exception as e:
        tb = traceback.format_exc()
        logging.error("Exception during upload: %s\n%s", str(e), tb)
        return jsonify({"error": "Failed to save file", "details": str(e)}), 500



if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("PORT") or os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") in ("1", "true", "True")
    app.run(host=host, port=port, debug=debug)
