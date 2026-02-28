from django.shortcuts import get_object_or_404, redirect, render
from .models import UserProfile, DailyLog, FoodEntry, ActivityEntry
from .forms import UserProfileForm, FoodEntryForm, ActivityEntryForm
from datetime import date, datetime, timedelta
# from django.contrib import messages
# from django.db.models import Sum
from .utils import calculate_activity_calories, calculate_bmr


def user_list(request):
    users = UserProfile.objects.all().order_by("id")
    return render(request, "users/user_list.html", {"users": users})

def user_create(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("user_detail", user_id=user.id)
    else:
        form = UserProfileForm()

    return render(request, "users/user_form.html", {"form": form})


def user_detail(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    return render(request, "users/user_detail.html", {"user": user})


def user_delete(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == "POST":
        user.delete()
        return redirect("user_list")

    return render(request, "users/user_confirm_delete.html", {"user": user})


def daily_tracking(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    # 1) Read date from query param (default today)
    date_str = request.GET.get("date")
    if date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        selected_date = date.today()

    # 2) Enforce: today and up to 30 days back (PDF)
    if selected_date > date.today() or selected_date < (date.today() - timedelta(days=30)):
        selected_date = date.today()

    # 3) Get or create DailyLog
    daily_log, _ = DailyLog.objects.get_or_create(user=user, date=selected_date)

    # 4) Default empty forms
    food_form = FoodEntryForm()
    activity_form = ActivityEntryForm()

    # 5) Handle POST (add entries)
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "food":
            food_form = FoodEntryForm(request.POST)
            if food_form.is_valid():
                entry = food_form.save(commit=False)
                entry.daily_log = daily_log
                entry.calories = float(entry.servings) * float(entry.food.calories_per_serving)
                entry.save()
                return redirect(f"{request.path}?date={selected_date.isoformat()}")

        elif form_type == "activity":
            activity_form = ActivityEntryForm(request.POST)
            if activity_form.is_valid():
                entry = activity_form.save(commit=False)
                entry.daily_log = daily_log
                entry.calories = calculate_activity_calories(
                    activity=entry.activity,
                    weight_kg=user.weight_kg,
                    duration_minutes=entry.duration_minutes,
                )
                entry.save()
                return redirect(f"{request.path}?date={selected_date.isoformat()}")

    # 6) Load existing entries
    food_entries = FoodEntry.objects.filter(daily_log=daily_log).select_related("food")
    activity_entries = ActivityEntry.objects.filter(daily_log=daily_log).select_related("activity")

    # 7) Compute totals + BMR + net
    total_food = sum(float(e.calories or 0) for e in food_entries)
    total_activity = sum(float(e.calories or 0) for e in activity_entries)
    bmr = calculate_bmr(user, selected_date)
    net = total_food - bmr - total_activity

    # (Optional) store on DailyLog (allowed: stored or calculated)
    daily_log.total_calories_in = total_food
    daily_log.total_activity_calories = total_activity
    daily_log.bmr_calculated = bmr
    daily_log.net_calories = net
    daily_log.save()

    context = {
        "user": user,
        "selected_date": selected_date,
        "food_form": food_form,
        "activity_form": activity_form,
        "food_entries": food_entries,
        "activity_entries": activity_entries,
        "total_food": total_food,
        "total_activity": total_activity,
        "bmr": bmr,
        "net": net,
    }
    return render(request, "tracking/daily_tracking.html", context)