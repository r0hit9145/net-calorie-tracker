# Net Calorie Tracker (Django)

A Django MVT web app to track daily net calories per user:

**Net Calories = Food Calories In − BMR − Activity Calories Out**

## Features (per assignment)
- User management:
  - Create user (name, weight, height, sex, date of birth)
  - List users
  - View details
  - Delete user (with confirmation)
- Import static datasets (XLSX):
  - Food dataset into `Food` table
  - Activity MET dataset into `Activity` table
- Daily tracking:
  - Select a user and a date (today up to 30 days back)
  - Add multiple food entries (food dropdown, servings, meal time) and see total calories in
  - Add multiple activity entries (activity dropdown, duration minutes) and see total calories out
  - Automatically calculate BMR using the provided formulas
  - Show Net Calories clearly and persist daily logs
- Date navigation:
  - Switch between dates and load existing logs

## Tech stack
- Python 3
- Django
- HTML/CSS/JS (Django templates)
- SQLite (default)

## Project setup (Linux)
```bash
git clone <https://github.com/r0hit9145/net-calorie-tracker.git>
cd <net-calorie-tracker>

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt
python manage.py migrate