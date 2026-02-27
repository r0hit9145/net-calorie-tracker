from django.db import models

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


MEAL_TIME_CHOICES = (
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Snack', 'Snack'),
)

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    weight_kg = models.FloatField()
    height_cm = models.FloatField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=200)
    serving_size = models.CharField(max_length=100)
    calories_per_serving = models.IntegerField()

    def __str__(self):
        return self.name
    

class Activity(models.Model):
    name = models.CharField(max_length=200)
    specific_motion = models.CharField(max_length=200)
    met_value = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.specific_motion}"
    

class DailyLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField()

    total_calories_in = models.FloatField(null=True, blank=True)
    total_activity_calories = models.FloatField(null=True, blank=True)
    bmr_calculated = models.FloatField(null=True, blank=True)
    net_calories = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.name} - {self.date}"
    
class FoodEntry(models.Model):
    daily_log = models.ForeignKey(DailyLog, on_delete=models.CASCADE, related_name='food_entries')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    servings = models.FloatField()
    meal_time = models.CharField(max_length=20, choices=MEAL_TIME_CHOICES)
    calories = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.food.name} x {self.servings} ({self.meal_time})"
    
class ActivityEntry(models.Model):
    daily_log = models.ForeignKey(DailyLog, on_delete=models.CASCADE, related_name='activity_entries')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    duration_minutes = models.FloatField()
    calories = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.activity.name} for {self.duration_minutes} min"