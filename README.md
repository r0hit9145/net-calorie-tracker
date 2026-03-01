# Net Calorie Tracker (Django)

A Django MVT web app to track daily net calories per user (Food calories in − BMR − Activity calories out).

# Features (per assignment)
- User management: create user, list users, view details, delete user. 
- Import static datasets:
  - Food dataset (XLSX) into `Food` table.
  - Activity MET dataset (XLSX) into `Activity` table.

- Daily tracking:
  - Select a user and a date (today up to 30 days back).
  - Add multiple food entries (food dropdown, servings, meal time) and see total calories in.
  - Add multiple activity entries (activity dropdown, duration minutes) and see total calories out.
  - Automatically calculate BMR using the provided formulas.
  - Show Net Calories clearly and persist daily logs.

- Date navigation to switch between days and load existing logs.

# Tech stack
- Python 3
- Django
-(HTML/CSS/JS)
- SQLite (default)

# Project setup (Linux)
```bash
git clone <YOUR_REPO_URL>
cd <YOUR_PROJECT_FOLDER>

python3 -m venv env
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate```


# Import datasets section
- python manage.py runserver
- Create a new user from the User List page.

- Open Daily Tracking for that user.

- Select a date (today to 30 days back).

- Add 1 food entry and 1 activity entry.

- Confirm totals, BMR, and Net Calories update and persist when reloading the same date.

- Use this exact block (paste after the setup section):

```md
## Import the Excel datasets
Make sure these files exist (relative to `manage.py`):

```text
data_excels/food-calories.xlsx
data_excels/MET-values.xlsx