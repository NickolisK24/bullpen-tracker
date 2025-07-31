def fatigue_color(fatigue):
    if fatigue < 40:
        return "🟢 Rested"
    elif fatigue < 80:
        return "🟡 Moderate"
    else:
        return "🔴 Overworked"
