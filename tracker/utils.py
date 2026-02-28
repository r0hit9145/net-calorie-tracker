from datetime import date
from .models import UserProfile, Activity

def calculate_age(dob: date, on_date: date) -> int:
    years = on_date.year - dob.year
    if (on_date.month, on_date.day) < (dob.month, dob.day):
        years -= 1
    return years


def calculate_bmr(user: UserProfile, on_date: date) -> float:
    age = calculate_age(user.date_of_birth, on_date)
    weight = float(user.weight_kg)
    height = float(user.height_cm)

    if user.sex == "M":
        # Men’s BMR formula (PDF)
        return 66.4730 + (13.7516 * weight) + (5.0033 * height) - (6.7550 * age)
    # Women’s BMR formula (PDF)
    return 655.0955 + (9.5634 * weight) + (1.8496 * height) - (4.6756 * age)


def calculate_activity_calories(activity: Activity, weight_kg: float, duration_minutes: float) -> float:
    # Calories burned by activity = MET × weight_kg × duration_hours (PDF)
    duration_hours = float(duration_minutes) / 60.0
    return float(activity.met_value) * float(weight_kg) * duration_hours