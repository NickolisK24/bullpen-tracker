from datetime import datetime
from dateutil.parser import parse

class Pitcher:
    def __init__(self, name, team, handedness=""):
        self.name = name
        self.team = team
        self.handedness = handedness
        self.games = []  # List of (date, pitch_count)

    def add_game(self, date_str, pitch_count):
        try:
            # Parse the date string flexibly (e.g., '2025-07-29', '7/29/2025', etc.)
            parsed = parse(date_str, fuzzy=False)
            # Normalize to date (strip time)
            date = datetime(parsed.year, parsed.month, parsed.day)
        except Exception as e:
            raise ValueError(f"Invalid date '{date_str}': {e}") from e
        self.games.append((date, pitch_count))

    def calculate_fatigue(self, current_date):
        # Normalize current_date to date only if it's datetime
        if isinstance(current_date, datetime):
            today = datetime(current_date.year, current_date.month, current_date.day)
        else:
            today = current_date
        fatigue = 0
        for game_date, pitch_count in self.games:
            days_rest = (today - game_date).days
            fatigue += pitch_count * max(0.2, 1 - days_rest * 0.15)
        return round(fatigue, 2)
