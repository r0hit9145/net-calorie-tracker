from django import forms
from .models import UserProfile, FoodEntry, ActivityEntry


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["name", "weight_kg", "height_cm", "sex", "date_of_birth"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ["food", "servings", "meal_time"]


class ActivityEntryForm(forms.ModelForm):
    class Meta:
        model = ActivityEntry
        fields = ["activity", "duration_minutes"]