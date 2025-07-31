# Bullpen Buddy / Pitcher Fatigue Tracker

A lightweight **MLB pitcher fatigue tracking tool** built as a portfolio project to showcase full-stack skills.  
It ingests historical pitch count data, computes a simple fatigue score per pitcher, and exposes that via a REST API for a React frontend to visualize and filter. This can be used by coaches, analysts, or front office staff to monitor workload and flag overuse risk.

## Live Demo
*(If deployed, put your live demo URL here, e.g.)*  
https://your-deployment.example.com

## Tech Stack

- **Backend:** Python, Flask, flask-cors  
- **Frontend:** React (can be plain JS or TypeScript), Tailwind CSS  
- **Data:** CSV upload of game logs (pitch counts, dates)  
- **Deployment candidates:** Vercel / Netlify (frontend), Render / Railway / Docker (backend)

## Features

- Upload a CSV of pitcher appearances.
- Compute a fatigue score per pitcher based on recent workload and rest.
- Filter/sort pitchers by team, name, fatigue range.
- Lookup an individual pitcher.
- Simple status indicator (e.g., rested / moderate / overworked).
- Configurable CORS origin via environment variable for integration.

## Fatigue Model

Fatigue is computed with a heuristic decay model:

For each appearance:
```
fatigue_contribution = pitch_count * max(0.2, 1 - days_rest * 0.15)
```

- Recent outings contribute more; the effect decays linearly with days of rest.
- A floor of `0.2` ensures very old appearances still leave a small residual.
- The total fatigue is the sum across all appearances, rounded for display.
- The fatigue is translated into a human-friendly status:
  - 🟢 Rested (low)
  - 🟡 Moderate
  - 🔴 Overworked (high)

This simple model is documented so future versions can replace or augment it with more sophisticated heuristics or learned risk models.

## Getting Started (Local Development)

### Prerequisites

- Python 3.10+ (or compatible)
- Node.js / npm or yarn (for frontend)
- Git

### Backend Setup

```bash
# from repository root
cd backend

# create & activate virtual env
python -m venv .venv
# Unix / Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run backend (defaults to localhost:5000)
python app.py
```

#### Environment variables (optional)
- `FRONTEND_ORIGIN` — allowed origin for CORS (default: `http://localhost:5173`)
- `FLASK_HOST` — host to bind (default: `0.0.0.0`)
- `FLASK_PORT` — port (default: `5000`)
- `FLASK_DEBUG` — `"1"` or `"true"` to enable debug mode

### Frontend Integration

Point your frontend at the backend. Example (Vite / React):

```js
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:5000";
```

Fetch all pitchers:

```
GET /api/pitchers
```

Filter by team or fatigue:

```
GET /api/pitchers?team=Yankees&min_fatigue=30&sort=name&order=asc
```

Fetch a single pitcher:

```
GET /api/pitchers/Clayton%20Kershaw
```

Upload a new CSV:

```
POST /api/upload
Form-data: file=<your CSV file>
```

### CSV Format

The backend expects a CSV file named (or uploaded to become) `game_logs.csv` with these columns:

| Column       | Description                          | Format / Notes                |
|--------------|--------------------------------------|-------------------------------|
| `name`       | Pitcher full name                    | e.g., "Jacob deGrom"          |
| `team`       | Team name                            | e.g., "New York Mets"         |
| `handedness` | Throws handedness                   | "R" or "L" (optional for logic)|
| `date`       | Date of appearance                  | `YYYY-MM-DD`                  |
| `pitch_count`| Number of pitches thrown            | Integer                      |

Example row:

```csv
name,team,handedness,date,pitch_count
Max Scherzer,New York Mets,R,2025-07-29,103
```

## API Endpoints Summary

- `GET /api/health` — basic health check.
- `GET /api/pitchers` — list all pitchers with fatigue. Supports query params:
  - `team` (substring match),
  - `min_fatigue`, `max_fatigue`,
  - `sort` (`fatigue` | `name` | `team`),
  - `order` (`asc` | `desc`),
  - `limit` (integer).
- `GET /api/pitchers/<name>` — exact name lookup (case-insensitive).
- `POST /api/upload` — upload a new CSV file; expects form-data file field.

## Example Usage

```bash
# List top 5 most fatigued pitchers
curl "http://localhost:5000/api/pitchers?sort=fatigue&order=desc&limit=5"

# Filter by team containing "Yankees"
curl "http://localhost:5000/api/pitchers?team=Yankees"

# Upload a new CSV
curl -F "file=@game_logs.csv" http://localhost:5000/api/upload
```

## Project Structure (simplified)

```
backend/
  app.py                 # Flask REST API
  pitcher.py             # Pitcher model and fatigue calculation
  fatigue_utils.py       # Helper for translating fatigue to statuses
  data/
    game_logs.csv       # Uploaded appearance data
  requirements.txt      # Python deps
frontend/
  src/                  # React components / API integration
  index.html
  tailwind.config.js
  ...
```

## Testing & Quality (Suggested)

- Add unit tests for:
  - Fatigue logic (`Pitcher.calculate_fatigue`)
  - CSV validation and edge cases.
  - API responses (happy path + error conditions).
- Linting: `flake8` / `black` for Python; ESLint / Prettier for frontend.
- CI pipeline (e.g., GitHub Actions) to run lint + tests on push.

## Future Enhancements

### Data & Insight
- **Fatigue Trends:** Show time series of a pitcher’s fatigue over their past N appearances.
- **Comparisons:** Side-by-side fatigue comparison between multiple pitchers or against a league average baseline.
- **Injury Risk Score:** Extend the heuristic into a learned or multi-factor model (e.g., logistic regression) to estimate injury/overuse probability.
- **Adaptive Recovery:** Incorporate rest recommendations based on upcoming schedule and current fatigue.

### Real-time & External Integration
- **Live MLB Data:** Pull pitch counts and appearance data from public APIs / scraping to auto-update without manual CSV uploads.
- **Schedule-awareness:** Cross-reference rotation schedules to flag when a fatigued pitcher is due to start soon.
- **Webhook/Notification System:** Alert on threshold crossings (e.g., fatigue > X) via email, Slack, or browser push.

### User/UX Features
- **Persistent Views:** Save favorite teams or custom filters in localStorage or user profiles.
- **Exportable Reports:** PDF/CSV summary of current fatigue status for a scouting report.
- **Dark Mode / Theming:** Toggleable theme that persists across sessions.
- **Search Autocomplete:** Typeahead for pitcher names.

### Engineering & Deployment
- **Dockerization:** Containerize backend and frontend for reproducible deployments.
- **Monorepo / Unified CLI:** Simplify `clone && run` with a one-command bootstrap (`make`, `setup.sh`).
- **Authentication:** If extended to user-specific saved views, add lightweight auth (OAuth / JWT).
- **Rate Limiting & Caching:** Protect public endpoints and speed up repeated queries.

### Code Quality
- **TypeScript migration (frontend):** Increase robustness of props, API contracts.
- **Schema validation:** Use tools like `pydantic` for strict backend input validation.
- **Swagger / OpenAPI docs:** Auto-generate API documentation for easier adoption.

### Accessibility & Polishing
- Keyboard navigable interface.
- ARIA labels and screen reader support.
- Mobile responsiveness.

## Deployment Suggestions

- **Frontend:** Vercel / Netlify – build the React/Tailwind app; inject `VITE_API_BASE` pointing to the backend.
- **Backend:** Render / Railway / Docker + Gunicorn. Use environment variables for configuration.
- **CI/CD:** GitHub Actions to:
  - Run backend tests.
  - Build frontend preview.
  - Deploy on merge to main.

## Contribution

This is primarily a personal portfolio project, but if you’re adapting it:
- Fork the repo.
- Follow the setup above.
- Open a PR with feature descriptions and test coverage.

## Contact

Built by **Nickolis Kacludis**.  
Portfolio: _[your site]_  
Email: _[your email]_
