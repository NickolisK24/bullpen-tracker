from datetime import datetime

class Pitcher:
    def __init__(self, name, team, handedness=""):
        self.name = name
        self.team = team
        self.handedness = handedness
        self.games = []  # List of (date, pitch_count)

    def add_game(self, date_str, pitch_count):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        self.games.append((date, pitch_count))

    def calculate_fatigue(self, current_date):
        fatigue = 0
        for game_date, pitch_count in self.games:
            days_rest = (current_date - game_date).days
            fatigue += pitch_count * max(0.2, 1 - days_rest * 0.15)
        return round(fatigue, 2)
