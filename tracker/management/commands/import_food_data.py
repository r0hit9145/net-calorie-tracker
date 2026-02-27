from django.core.management.base import BaseCommand
from tracker.models import Food
from pathlib import Path
import openpyxl


class Command(BaseCommand):
    help = "Import food-calories.xlsx into Food table"

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        file_path = base_dir / "data_excels" / "food-calories.xlsx"

        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        # Expected headers: ID, name, Food Group, Calories, ..., Serving Description 1 (g)
        rows = sheet.iter_rows(values_only=True)

        header = next(rows)  # first row
        # optional: print(header) once if you want to confirm
        # self.stdout.write(str(header))

        imported = 0
        for row in rows:
            if not row or not row[1]:
                continue

            name = str(row[1]).strip()              # column B
            calories = row[3]                       # column D
            serving_desc = row[7] if len(row) > 7 else None  # column H

            # basic cleaning
            if calories is None:
                continue

            Food.objects.update_or_create(    #this is exactly update or create if you find new record.
                name=name,
                defaults={
                    "serving_size": str(serving_desc).strip() if serving_desc else "",
                    "calories_per_serving": int(float(calories)),
                }
            )
            imported += 1

        self.stdout.write(self.style.SUCCESS(f"Imported/updated {imported} foods"))