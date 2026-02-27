from django.core.management.base import BaseCommand
from tracker.models import Activity
from pathlib import Path
import openpyxl


class Command(BaseCommand):
    help = "Import MET-values.xlsx into Activity table"

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        file_path = base_dir / "data_excels" / "MET-values.xlsx"

        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        rows = sheet.iter_rows(values_only=True)
        header = next(rows)  # first row

        imported = 0
        for row in rows:
            if not row or not row[0]:
                continue

            activity_name = str(row[0]).strip()         # column A
            specific_motion = str(row[1]).strip() if row[1] else ""  # column B

            # MET value is likely column C; if your sheet has it in a different column,
            # we will adjust after you confirm by scrolling right once.
            met_value = row[2] if len(row) > 2 else None
            if met_value is None:
                continue

            Activity.objects.update_or_create(
                name=activity_name,
                specific_motion=specific_motion,
                defaults={"met_value": float(met_value)},
            )
            imported += 1

        self.stdout.write(self.style.SUCCESS(f"Imported/updated {imported} activities"))